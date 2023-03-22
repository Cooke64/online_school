import React from 'react'
import { Route, Routes } from 'react-router-dom';

import MainPage from './MainPage';
import ErrorPapge from './ErrorPage';
import Layout from './Layout';



export default function AppRoutes() {
    return (
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="/" element={<MainPage />} />
          </Route>
          <Route path="*" element={<ErrorPapge />} />
        </Routes>
      );
}