import { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useAuthStore } from './stores/authStore';
import Header from './components/layout/Header';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ModulePage from './pages/ModulePage';
import LessonPage from './pages/LessonPage';
import ExercisePage from './pages/ExercisePage';
import Profile from './pages/Profile';

export default function App() {
  const { isAuthenticated, loadUser } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated) {
      loadUser();
    }
  }, [isAuthenticated, loadUser]);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-950">
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={<ProtectedRoute><Dashboard /></ProtectedRoute>}
          />
          <Route
            path="/module/:moduleSlug"
            element={<ProtectedRoute><ModulePage /></ProtectedRoute>}
          />
          <Route
            path="/module/:moduleSlug/lesson/:lessonSlug"
            element={<ProtectedRoute><LessonPage /></ProtectedRoute>}
          />
          <Route
            path="/module/:moduleSlug/lesson/:lessonSlug/exercise/:exerciseSlug"
            element={<ProtectedRoute><ExercisePage /></ProtectedRoute>}
          />
          <Route
            path="/profile"
            element={<ProtectedRoute><Profile /></ProtectedRoute>}
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
