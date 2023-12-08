import React, { lazy, Suspense } from 'react'
import { Route, Routes } from 'react-router-dom'

import NotFoundPage from './pages/NotFoundPage'
import ProtectedRoute from './routes/ProtectedRoute'

const Dashboard = lazy(() => import('./pages/Dashboard.tsx'))
const Webmaster = lazy(() => import('./pages/Webmaster.tsx'))
const Contact = lazy(() => import('./pages/Contact.tsx'))
const Project = lazy(() => import('./pages/Project.tsx'))
const PaymentHistory = lazy(() => import('./pages/PaymentHistory.tsx'))
const ProfileSettings = lazy(() => import('./pages/ProfileSettings.tsx'))
const Login = lazy(() => import('./pages/Login.tsx'))
const Registration = lazy(() => import('./pages/Registration.tsx'))

const pages = {
  Dashboard,
  Webmaster,
  Contact,
  Project,
  PaymentHistory,
  ProfileSettings,
  Login,
  Registration
}

const protectedRoutes = [
  { path: '/', component: 'Dashboard' },
  { path: '/webmasters/', component: 'Webmaster' },
  { path: '/contacts/', component: 'Contact' },
  { path: '/projects/', component: 'Project' },
  { path: '/payments/', component: 'PaymentHistory' },
  { path: '/profile-settings/', component: 'ProfileSettings' }
]

function App() {
  return (
    <Routes>
      {protectedRoutes.map(({ path, component }, index) => (
        <Route
          key={index}
          path={path}
          element={
            <ProtectedRoute>
              <Suspense fallback={<div>Loading...</div>}>
                {React.createElement(pages[component])}
              </Suspense>
            </ProtectedRoute>
          }
        />
      ))}
      {['Login', 'Registration'].map((component, index) => (
        <Route
          key={index}
          path={`/${component.toLowerCase()}/`}
          element={
            <Suspense fallback={<div>Loading...</div>}>
              {React.createElement(pages[component])}
            </Suspense>
          }
        />
      ))}
      <Route path='*' element={<NotFoundPage />} />
    </Routes>
  )
}

export default App
