import React from 'react'
import { Route, Routes } from 'react-router-dom';

import ErrorPapge from './ErrorPage';
import Layout from './Layout';
import HomePage from './HomePage/HomePage';
import AboutPage from './AboutPage/AboutPage';
import CourseDetail from './CourseDetail/CourseDetail';
import LessonDetail from './LessonDetail/LessonDetail';
import TeachersPage from './TeachersPage/TeachersPage';


export default function AppRoutes() {
    return (
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/teachers_list" element={<TeachersPage />} />
            <Route path="/course/:id" element={<CourseDetail />} />
            <Route path="/course/:course_id/lesson/:lesson_id" element={<LessonDetail />} />
          </Route>
          <Route path="*" element={<ErrorPapge />} />
        </Routes>
      );
}