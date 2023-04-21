import React from 'react'
import { Route, Routes } from 'react-router-dom';

import ErrorPapge from './ErrorPage';
import Layout from './Layout';
import HomePage from './HomePage/HomePage';
import AboutPage from './AboutPage/AboutPage';
import CourseDetail from './CourseDetail/CourseDetail';

export default function AppRoutes() {
    return (
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/course/:id" element={<CourseDetail />} />
          </Route>
          <Route path="*" element={<ErrorPapge />} />
        </Routes>
      );
}