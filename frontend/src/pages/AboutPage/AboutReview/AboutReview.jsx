import React from "react";
import cls from "./AboutReview.module.css";
import CourseBase from "../../../img/course_base.png";
export default function AboutReview() {
  return (
    <section>
      <h1 className='section_header'>AboutReview</h1>
      <div className={cls.box_container}>
        <div className={cls.box}>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Deserunt
            voluptate nulla iste reiciendis eius laborum tempore, atque
            provident. Voluptates earum accusantium, eveniet dignissimos
            officiis atque commodi voluptas. Nam, molestiae consequuntur.
            Ducimus magni veritatis fugiat odit. Molestias nulla animi, beatae
          </p>
          <div className={cls.user_review}>
            <img src={CourseBase} alt="about_pic" />
            <div>
              <h3>Some student</h3>
            </div>
          </div>
        </div>
        <div className={cls.box}>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Deserunt
            voluptate nulla iste reiciendis eius laborum tempore, atque
            provident. Voluptates earum accusantium, eveniet dignissimos
            officiis atque commodi voluptas. Nam, molestiae consequuntur.
            Ducimus magni veritatis fugiat odit. Molestias nulla animi, beatae
          </p>
          <div className={cls.user_review}>
            <img src={CourseBase} alt="about_pic" />
            <div>
              <h3>Some student</h3>
            </div>
          </div>
        </div>
        <div className={cls.box}>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Deserunt
            voluptate nulla iste reiciendis eius laborum tempore, atque
            provident. Voluptates earum accusantium, eveniet dignissimos
            officiis atque commodi voluptas. Nam, molestiae consequuntur.
            Ducimus magni veritatis fugiat odit. Molestias nulla animi, beatae
          </p>
          <div className={cls.user_review}>
            <img src={CourseBase} alt="about_pic" />
            <div>
              <h3>Some student</h3>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
