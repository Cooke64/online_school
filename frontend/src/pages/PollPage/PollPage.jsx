import React from "react";
import PollItem from "./PollItem";
import cls from "./Poll.module.css";
import BaseButton from "../../components/UI/BaseButton/BaseButton";
export default function PollPage() {
  const questions = [
    {
      id: 1,
      question_text: "what is that?",
      answers_list: [
        {
          id: 1,
          answer_text: "str",
          is_correct: true,
        },
        {
          id: 2,
          answer_text: "tuple",
          is_correct: false,
        },
        {
          id: 3,
          answer_text: "bool",
          is_correct: false,
        },
        {
          id: 4,
          answer_text: "int",
          is_correct: true,
        },
      ],
    },
    {
      id: 2,
      question_text: "where is mistake?",
      answers_list: [
        {
          id: 1,
          answer_text: "str",
          is_correct: true,
        },
        {
          id: 2,
          answer_text: "tuple",
          is_correct: false,
        },
        {
          id: 3,
          answer_text: "bool",
          is_correct: false,
        },
        {
          id: 4,
          answer_text: "int",
          is_correct: true,
        },
      ],
    },
  ];
  const [currentQuestion, setCurrentQuestion] = React.useState(0);
  const [counterCorrectAnswer, setCounterCorrectAnswer] = React.useState(0);
  const [hasfinished, setHasFinished] = React.useState(false);
  React.useEffect(() => {}, [currentQuestion]);
  const handlerAnswer = (answer) => {
    if (answer.is_correct) {
        setCounterCorrectAnswer(counterCorrectAnswer + 1)
    }
    const newQuestion = currentQuestion + 1;
    if (newQuestion < questions.length) {
      setCurrentQuestion(newQuestion);
    } else {
      setHasFinished(true);
    }
  };
  const startAgainHandker = () => {
    setHasFinished(false);
    setCurrentQuestion(0);
    setCounterCorrectAnswer(0)
  }
  return (
    <section>
      <h1 className="section_header">
        {hasfinished ? "Прошли тестирование" : "Тестирование пройденного урока"}
      </h1>

      {hasfinished ? (
        <div className={cls.box}>
          <h3>Ваш результат: {counterCorrectAnswer} из {questions.length}</h3>
          <BaseButton className={"btn_inline"} onClick={startAgainHandker}>
            Начать заново?
          </BaseButton>
        </div>
      ) : (
        <>
          <h3>
            Вопрос {currentQuestion + 1} из {questions.length}
          </h3>
          <PollItem
            question={questions[currentQuestion]}
            handlerAnswer={handlerAnswer}
          />
        </>
      )}
    </section>
  );
}
