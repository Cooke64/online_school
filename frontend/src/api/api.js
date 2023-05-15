/* eslint-disable import/no-anonymous-default-export */
class Api {
  constructor(headers) {
    this.headers = headers
  }


  checkResponse(res) {
    return new Promise((resolve, reject) => {
      const func = res.status < 400 ? resolve : reject
      res.json().then(data => {
        func(data)
      })
    })
  }

  // Course crud

  getCoursesList() {
    return fetch(
        `http://127.0.0.1:8000/course/`, {
          method: 'GET',
        }
      )
      .then(this.checkResponse)
  }
  getCourseDetail(id) {
    return fetch(
        `http://127.0.0.1:8000/course/` + id, {
          method: 'GET',
        }
      )
      .then(this.checkResponse)
  }

  createNewCourse(course) {
    const token = localStorage.getItem('token')
    return fetch(
        `http://127.0.0.1:8000/course/`, {
          method: 'POST',
          headers: {
            ...this.headers,
            'Authorization': token
          },
          body: JSON.stringify(course)
        }
      )
      .then(this.checkResponse)
  }

  removeCourse(
    course_id
  ) {
    const token = localStorage.getItem('token')
    return fetch(
      `http://127.0.0.1:8000/course/${course_id}`, {
        method: 'delete',
        headers: {
          ...this.headers,
          'Authorization': token
        },
      }
    ).then(this.checkResponse)
  }

  // Lesson crud

  getLessonDetail(course_id, lesson_id) {
    const token = localStorage.getItem('token')
    return fetch(
        `http://127.0.0.1:8000/lesson/${course_id}/${lesson_id}`, {
          method: 'GET',
          headers: {
            ...this.headers,
            'Authorization': token
          },
        }
      )
      .then(this.checkResponse)
  }

  addLessonToCourse(course_id, lessonData) {
    const token = localStorage.getItem('token')
    return fetch(
        `http://127.0.0.1:8000/lesson/${course_id}`, {
          method: 'POST',
          headers: {
            ...this.headers,
            'Authorization': token
          },
          body: JSON.stringify(lessonData)
        }
      )
      .then(this.checkResponse)
  }
  addPhotoToLesson(lessonId, selectedImage) {
    const formData = new FormData();
    formData.append("photo", selectedImage, selectedImage.name);
    return fetch(
        `http://127.0.0.1:8000/lesson/content/${lessonId}/upload_photo`, {
          method: 'POST',
          body:formData
        }
      )
      .then(this.checkResponse)
  }
  // Teacher crud

  getTeachersList() {
    return fetch(
        `http://127.0.0.1:8000/teachers/`, {
          method: 'GET',
        }
      )
      .then(this.checkResponse)
  }
  getTeachersDeatil(teacher_id) {
    console.log(teacher_id)
    return fetch(
        `http://127.0.0.1:8000/teachers/` + teacher_id, {
          method: 'GET',
        }
      )
      .then(this.checkResponse)
  }

  loginUser({
    email,
    password
  }) {
    const body = JSON.stringify({
      email,
      password
    })
    return fetch(
      `http://127.0.0.1:8000/user/login`, {
        method: 'post',
        headers: this.headers,
        body: body
      }
    ).then(this.checkResponse)
  }

  getMe() {
    const token = localStorage.getItem('token')
    return fetch(
      `http://127.0.0.1:8000/user/me`, {
        method: 'get',
        headers: {
          ...this.headers,
          'Authorization': token
        },
      }
    ).then(this.checkResponse)
  }
  addComment(
    course_id,
    lesson_id,
    text
  ) {
    const token = localStorage.getItem('token')
    const body = JSON.stringify({
      text
    })
    return fetch(
      `http://127.0.0.1:8000/lesson/${course_id}/${lesson_id}/add_comment`, {
        method: 'post',
        headers: {
          ...this.headers,
          'Authorization': token
        },
        body: body
      }
    ).then(this.checkResponse)
  }
  removeComment(
    lesson_id,
    comment_id,
  ) {
    const token = localStorage.getItem('token')
    return fetch(
      `http://127.0.0.1:8000/lesson/${lesson_id}/remove_comment/${comment_id}`, {
        method: 'delete',
        headers: {
          ...this.headers,
          'Authorization': token
        },
      }
    ).then(this.checkResponse)
  }
  getStudentProfile() {
    const token = localStorage.getItem('token')
    return fetch(
      `http://127.0.0.1:8000/student/my_courses`, {
        method: 'get',
        headers: {
          ...this.headers,
          'Authorization': token
        },
      }
    ).then(this.checkResponse)

  }
  getPassedLessons() {
    const token = localStorage.getItem('token')
    return fetch(
      `http://127.0.0.1:8000/student/passed_lessons`, {
        method: 'get',
        headers: {
          ...this.headers,
          'Authorization': token
        },
      }
    ).then(this.checkResponse)

  }

}


export default new Api({
  'content-type': 'application/json',
  'accept': 'application/json',
  "Access-Control-Allow-Origin": "*"

})