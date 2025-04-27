import asyncio
import re
from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db, SessionLocal
from gemini_config.models.gemini_model import Gemini
import google.generativeai as genai

from multiple_choice_questions.models.choice_model import Choice
from multiple_choice_questions.models.question_model import Question


class GeminiServices:
    async def get_access_token_available(self,  db: Session = Depends(get_db)):
        return db.query(Gemini).filter(Gemini.last_expired_at < datetime.now(timezone.utc)).first().access_token

    async def question_generator(self, input_text: str, db):
        access_token = await self.get_access_token_available(db)
        genai.configure(api_key=access_token)
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        prompt = f"""
            You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
            '{input_text}'
            Please generate 1 MCQ from the text. Question should have:
            - A clear question
            - Four answer options (labeled A, B, C, D)
            - The correct answer clearly indicated
            - An explanation for why the correct answer is right
            Format:
            Question: [question]
            A) [option A]
            B) [option B]
            C) [option C]
            D) [option D]
            Correct Answer: [correct option]
            Explanation: [brief explanation]
            """
        response = model.generate_content(prompt).text.strip()
        return response

    def parse_mcq_to_objects(self, mcq_text: str):
        question_match = re.search(r"Question:\s*(.+)", mcq_text)
        explanation_match = re.search(r"Explanation:\s*(.+)", mcq_text, re.DOTALL)
        correct_match = re.search(r"Correct Answer:\s*([A-D])", mcq_text)

        choices_match = re.findall(r"([A-D])\)\s*(.+)", mcq_text)

        if not (question_match and explanation_match and correct_match and len(
                choices_match) == 4):
            raise ValueError("MCQ text is not in the correct format")

        question_text = question_match.group(1).strip()
        explanation_text = explanation_match.group(1).strip()
        correct_letter = correct_match.group(1).strip()

        # Tạo câu hỏi
        question_obj = Question(
            question=question_text,
            explanation=explanation_text,
        )

        choice_objects = []
        for letter, content in choices_match:
            choice_obj = Choice(
                content=content.strip(),
                is_best_choice=(letter == correct_letter),
            )
            choice_objects.append(choice_obj)

        # Gắn mối quan hệ
        question_obj.choices = choice_objects

        return question_obj


async def main():
    gemini_service = GeminiServices()

    db = SessionLocal()

    input_text = "Gravity is the force that attracts two bodies towards each other. It is responsible for keeping planets in orbit around the sun and governs the motion of objects on Earth."

    generated_mcq_text = await gemini_service.question_generator(input_text, db)
    print("Generated MCQ Text:\n", generated_mcq_text)

    question_obj = gemini_service.parse_mcq_to_objects(generated_mcq_text)

    try:
        db.add(question_obj)
        db.commit()
        db.refresh(question_obj)
        print(f"\nSaved Question ID: {question_obj.id}")
    except Exception as e:
        db.rollback()
        print("Error saving to DB:", str(e))
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
