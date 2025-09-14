import React from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './styles.css'
import App from './pages/App'
import Course from './pages/Course'
import NotFound from './pages/NotFound'
import Login from './pages/Login'
import Register from './pages/Register'
import Courses from './pages/Courses'
import Lesson from './pages/Lesson'
import Chat from './pages/Chat'
import Practice from './pages/Practice'
import Admin from './pages/Admin'

const router = createBrowserRouter([
  { path: '/', element: <App /> },
  { path: '/login', element: <Login /> },
  { path: '/register', element: <Register /> },
  { path: '/courses', element: <Courses /> },
  { path: '/courses/:id', element: <Course /> },
  { path: '/lessons/:id', element: <Lesson /> },
  { path: '/chat/:chatId', element: <Chat /> },
  { path: '/practice', element: <Practice /> },
  { path: '/admin', element: <Admin /> },
  { path: '*', element: <NotFound /> },
])

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)
