import {
  getFormGroupUtilityClass
} from "@mui/material"

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

  // post CRUD

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
        `http://127.0.0.1:8000/course/` + id,
         {
          method: 'GET',
        }
      )
      .then(this.checkResponse)
  }
  getLessonDetail(course_id, lesson_id) {
    return fetch(
        `http://127.0.0.1:8000/lesson/content/${course_id}/${lesson_id}`,
         {
          method: 'GET',
        }
      )
      .then(this.checkResponse)
  }
}


export default new Api({
  'content-type': 'application/json',
  'accept': 'application/json'

})