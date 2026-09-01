import React, { useState, useEffect } from 'react';
import { useTheme } from '../components/ThemeProvider';
import { useTranslation } from '../i18n.jsx';
import { Flame, Sun, Moon, Youtube, Instagram, Share2, MessageCircle } from 'lucide-react';

const Layout = ({ children }) => {
  const { isDark, toggleTheme } = useTheme();
  const { t, lang, setLang } = useTranslation();
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePos({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const toggleLanguage = () => {
    setLang(lang === 'en' ? 'id' : 'en');
  };

  return (
    <div className={`min-h-screen transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${isDark ? 'bg-[#131314] text-white' : 'bg-[#F0F4F9] text-[#1F1F1F]'}`}>
      {/* Interactive Cursor Spotlight */}
      <div 
        className="pointer-events-none fixed inset-0 z-50 transition-opacity duration-300"
        style={{
          background: `radial-gradient(600px circle at ${mousePos.x}px ${mousePos.y}px, ${isDark ? 'rgba(220,38,38,0.06)' : 'rgba(220,38,38,0.04)'}, transparent 40%)`
        }}
      />

      {/* Ambient Background Aura - Gemini Luminous Effect */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        {isDark ? (
          <>
            <div className="absolute -top-[10%] -left-[10%] w-[50vw] h-[50vw] rounded-full bg-crimson-700/20 mix-blend-screen blur-[120px] animate-blob"></div>
            <div className="absolute top-[20%] -right-[10%] w-[45vw] h-[45vw] rounded-full bg-indigo-600/20 mix-blend-screen blur-[120px] animate-blob animation-delay-2000"></div>
            <div className="absolute -bottom-[20%] left-[20%] w-[55vw] h-[55vw] rounded-full bg-rose-800/20 mix-blend-screen blur-[120px] animate-blob animation-delay-4000"></div>
          </>
        ) : (
          <>
            <div className="absolute -top-[10%] -left-[10%] w-[50vw] h-[50vw] rounded-full bg-rose-300/40 mix-blend-multiply blur-[120px] animate-blob"></div>
            <div className="absolute top-[20%] -right-[10%] w-[45vw] h-[45vw] rounded-full bg-blue-300/40 mix-blend-multiply blur-[120px] animate-blob animation-delay-2000"></div>
            <div className="absolute -bottom-[20%] left-[20%] w-[55vw] h-[55vw] rounded-full bg-amber-200/40 mix-blend-multiply blur-[120px] animate-blob animation-delay-4000"></div>
          </>
        )}
      </div>

      {/* Main Content Wrapper to sit above the aura */}
      <div className="relative z-10 flex flex-col min-h-screen">

      {/* Navbar */}
      <nav className="sticky top-0 z-50 backdrop-blur-md border-b border-transparent">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <Flame className="w-8 h-8 text-crimson-600" />
              <span className="font-bold text-xl tracking-tight">ZIYAN</span>
            </div>
            
            <div className="hidden md:flex space-x-2">
              <a href="#products" className={`px-4 py-2 rounded-full transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${isDark ? 'hover:bg-white/10' : 'hover:bg-black/5'}`}>{t('nav_products') || 'Products'}</a>
              <a href="#about" className={`px-4 py-2 rounded-full transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${isDark ? 'hover:bg-white/10' : 'hover:bg-black/5'}`}>{t('nav_about') || 'About'}</a>
            </div>

            <div className="flex items-center space-x-2">
              <button onClick={toggleLanguage} className={`px-3 py-1.5 rounded-full text-sm font-medium transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${isDark ? 'bg-white/10 hover:bg-white/20' : 'bg-black/5 hover:bg-black/10'}`}>
                {lang ? lang.toUpperCase() : 'EN'}
              </button>
              <button onClick={toggleTheme} className={`p-2 rounded-full transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${isDark ? 'bg-white/10 hover:bg-white/20' : 'bg-black/5 hover:bg-black/10'}`}>
                {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main>{children}</main>

      {/* Footer */}
      <footer className="py-12 mt-20 text-center">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-center items-center gap-2 mb-4">
            <Flame className="w-6 h-6 text-crimson-600" />
            <span className="font-bold text-lg">ZIYAN</span>
          </div>
          <p className={`mb-6 text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Official Store: <a href="https://lynk.id/yang_mulia" target="_blank" rel="noopener noreferrer" className="text-crimson-500 hover:underline font-semibold">lynk.id/yang_mulia</a></p>
          <div className="flex justify-center space-x-4 mb-8">
            <a href="https://youtube.com/@abangjal" target="_blank" rel="noopener noreferrer" title="YouTube" className={`p-2.5 rounded-full transition-all duration-300 ${isDark ? 'hover:bg-white/10 text-gray-300' : 'hover:bg-black/5 text-gray-700'}`}><Youtube className="w-5 h-5" /></a>
            <a href="https://instagram.com/abangjal" target="_blank" rel="noopener noreferrer" title="Instagram" className={`p-2.5 rounded-full transition-all duration-300 ${isDark ? 'hover:bg-white/10 text-gray-300' : 'hover:bg-black/5 text-gray-700'}`}><Instagram className="w-5 h-5" /></a>
            <a href="https://tiktok.com/@abangjal" target="_blank" rel="noopener noreferrer" title="TikTok" className={`p-2.5 rounded-full transition-all duration-300 ${isDark ? 'hover:bg-white/10 text-gray-300' : 'hover:bg-black/5 text-gray-700'}`}><Share2 className="w-5 h-5" /></a>
            <a href="https://wa.me/6282268157023" target="_blank" rel="noopener noreferrer" title="WhatsApp" className={`p-2.5 rounded-full transition-all duration-300 ${isDark ? 'hover:bg-white/10 text-gray-300' : 'hover:bg-black/5 text-gray-700'}`}><MessageCircle className="w-5 h-5" /></a>
          </div>
          <p className={`text-sm ${isDark ? 'text-gray-500' : 'text-gray-400'}`}>&copy; {new Date().getFullYear()} ZiyanCorp. {t('footer_copyright') || 'All rights reserved.'}</p>
        </div>
      </footer>
      </div>
    </div>
  );
};

export default Layout;
