class Api {
  constructor(headers) {
    this.headers = headers
    this.baseURL = "http://localhost:8000/api";
  }


  checkResponse(res) {
    return new Promise((resolve, reject) => {
      const func = res.status < 400 ? resolve : reject
      res.json().then(data => {
        func(data)
      })
    })
  }


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
  getLessonDetail(course_id, lesson_id) {
    return fetch(
        `http://127.0.0.1:8000/lesson/${course_id}/${lesson_id}`, {
          method: 'GET',
        }
      )
      .then(this.checkResponse)
  }
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
  createnewCourse(course) {
    const token = localStorage.getItem('token')
    return fetch(
        `http://127.0.0.1:8000/course/`, {
          method: 'POST',
          headers: {
            ...this.headers,
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(course)
        }
      )
      .then(this.checkResponse)
  }

}


export default new Api({
  'content-type': 'application/json',
  'accept': 'application/json'

})