import React from 'react';
import { useTranslation } from '../i18n.jsx';
import { useTheme } from '../components/ThemeProvider';
import { ArrowDown } from 'lucide-react';

const HeroSection = () => {
  const { t } = useTranslation();
  const { isDark } = useTheme();

  const handleScroll = () => {
    document.getElementById('products')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className="w-full py-16 lg:py-24 px-4 sm:px-6 lg:px-8 flex flex-col items-center text-center relative">
      {/* Luminous Glow Badge */}
      <div className="animate-fade-in-up relative group" style={{ animationDelay: '0ms', animationFillMode: 'both' }}>
        <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-crimson-600/50 via-violet-600/40 to-cyan-500/50 blur-md opacity-70 group-hover:opacity-100 transition-opacity duration-500 animate-pulse"></div>
        <div className="relative inline-flex items-center gap-2 px-5 py-2 rounded-full text-xs sm:text-sm font-semibold tracking-wide backdrop-blur-xl border border-white/20 bg-[#1E1F20]/80 text-white shadow-[0_0_15px_rgba(220,38,38,0.3)]">
          <span className="w-2 h-2 rounded-full bg-crimson-500 animate-ping"></span>
          <span>✨ ZiyanCorp Luminous Design</span>
        </div>
      </div>
      
      <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold font-display mt-8 mb-6 tracking-tight animate-fade-in-up max-w-4xl" style={{ animationDelay: '100ms', animationFillMode: 'both' }}>
        {t('hero_title')?.split('Creators').map((part, i, arr) => (
          <React.Fragment key={i}>
            {part}
            {i < arr.length - 1 && (
              <span className="text-transparent bg-clip-text bg-[conic-gradient(from_0deg,#DC2626_0%,#8B5CF6_35%,#06B6D4_70%,#F43F5E_90%,#DC2626_100%)]">
                Creators
              </span>
            )}
          </React.Fragment>
        )) || (
          <>Empowering <span className="text-transparent bg-clip-text bg-[conic-gradient(from_0deg,#DC2626_0%,#8B5CF6_35%,#06B6D4_70%,#F43F5E_90%,#DC2626_100%)]">Creators</span> Worldwide</>
        )}
      </h1>
      
      <p className={`max-w-2xl text-lg sm:text-xl mb-10 animate-fade-in-up ${isDark ? 'text-gray-300' : 'text-gray-600'}`} style={{ animationDelay: '200ms', animationFillMode: 'both' }}>
        {t('hero_subtitle') || 'Premium digital tools, templates, and resources designed to accelerate your workflow and elevate your next big project.'}
      </p>
      
      {/* Luminous CTA Button with Spectral Rotating Edge */}
      <div className="relative group animate-fade-in-up" style={{ animationDelay: '300ms', animationFillMode: 'both' }}>
        <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-crimson-600 via-violet-600 to-cyan-500 blur-lg opacity-60 group-hover:opacity-100 transition-opacity duration-500 animate-pulse"></div>
        <button 
          onClick={handleScroll}
          className="relative flex items-center gap-2.5 px-8 py-4 rounded-full bg-gradient-to-r from-crimson-600 to-rose-600 hover:from-crimson-500 hover:to-rose-500 text-white font-semibold shadow-2xl hover:scale-105 transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] border border-white/20"
        >
          <span>{t('hero_cta') || 'Explore Products'}</span>
          <ArrowDown className="w-5 h-5 animate-bounce" />
        </button>
      </div>
      
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in-up {
          animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }
      `}} />
    </section>
  );
};

export default HeroSection;
