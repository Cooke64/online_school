import React from 'react'
import { Route, Routes } from 'react-router-dom';

import ErrorPapge from './ErrorPage';
import Layout from './Layout';
import HomePage from './HomePage/HomePage';



export default function AppRoutes() {
    return (
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="/" element={<HomePage />} />
          </Route>
          <Route path="*" element={<ErrorPapge />} />
        </Routes>
      );
}