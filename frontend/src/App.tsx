import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useThemeStore } from './stores/themeStore';
import Header from './components/layout/Header';
import Home from './pages/Home';
import StyleGuide from './pages/StyleGuide';

function App() {
  const { isDarkMode, setDarkMode } = useThemeStore();

  useEffect(() => {
    // Initialize theme on app start
    const savedTheme = localStorage.getItem('theme-storage');
    if (savedTheme) {
      const parsed = JSON.parse(savedTheme);
      setDarkMode(parsed.state?.isDarkMode ?? true);
    } else {
      // Default to dark mode
      setDarkMode(true);
    }
  }, [setDarkMode]);

  return (
    <div className={isDarkMode ? 'dark' : 'light'}>
      <div className="min-h-screen bg-dark-900 text-dark-50 transition-colors duration-200 flex flex-col">
        <Router>
          <Header />
          <main className="flex-1 flex flex-col">
            <Routes>
              <Route path="/" element={
                <div className="flex-1 flex flex-col container mx-auto px-4 py-6">
                  <Home />
                </div>
              } />
              <Route path="/styleguide" element={
                <div className="container mx-auto px-4 py-6">
                  <StyleGuide />
                </div>
              } />
            </Routes>
          </main>
        </Router>
      </div>
    </div>
  );
}

export default App;