import React from "react";
import PollItem from "./PollItem";
import cls from "./Poll.module.css";
import BaseButton from "../../components/UI/BaseButton/BaseButton";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import api from "../../api/api";
import { useParams } from "react-router-dom";
import Loader from "../../components/UI/Loader/Loader";

export default function PollPage() {
  const { course_id, lesson_id } = useParams();
  const [isLoading, setIsLoading] = React.useState(true);
  const [questions, setQuestions] = React.useState([]);
  const [currentQuestion, setCurrentQuestion] = React.useState(0);
  const [counterCorrectAnswer, setCounterCorrectAnswer] = React.useState(0);
  const [hasfinished, setHasFinished] = React.useState(false);
  const [needPassPoll, setNeedPassPoll] = React.useState(2);

  React.useEffect(() => {
    console.log("res");
    api.getLessonPoll(lesson_id).then((res) => {
      setQuestions(res.question_list);
      setIsLoading(false);
    });
  }, [lesson_id]);

  React.useEffect(() => {
    if (needPassPoll === counterCorrectAnswer) {
      console.log("123");
      // api.makeLessonPass()
    }
  }, [currentQuestion, counterCorrectAnswer, needPassPoll]);

  const handlerAnswer = (answer) => {
    if (answer.is_correct) {
      setCounterCorrectAnswer(counterCorrectAnswer + 1);
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
    setCounterCorrectAnswer(0);
  };
  return (
    <section>
      <h1 className="section_header">
        {hasfinished ? "Прошли тестирование" : "Тестирование пройденного урока"}
      </h1>
      {hasfinished ? (
        <div className={cls.box}>
          <h3>
            Ваш результат: {counterCorrectAnswer} из {questions.length}
          </h3>
          <BaseButton className={"btn_inline"} onClick={startAgainHandker}>
            Начать заново?
          </BaseButton>
          {needPassPoll === counterCorrectAnswer && (
            <ButtonAsLink
              to="/courses"
              button_type="inline"
              btn_action="option"
            >
              К следующему уроку
            </ButtonAsLink>
          )}
        </div>
      ) : (
        <>
          <h3>
            Вопрос {currentQuestion + 1} из {questions.length}
          </h3>
          {isLoading ? (
            <div>
              <Loader />
            </div>
          ) : (
            <PollItem
              question={questions[currentQuestion]}
              handlerAnswer={handlerAnswer}
            />
          )}
        </>
      )}
    </section>
  );
}
