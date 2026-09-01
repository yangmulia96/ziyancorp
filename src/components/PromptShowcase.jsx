import React from 'react';
import { useTranslation } from '../i18n.jsx';
import { useTheme } from '../components/ThemeProvider';
import { Lock, Play, Clock, Sparkles, Type, Globe } from 'lucide-react';

const Badge = ({ icon: Icon, label }) => {
  const { isDark } = useTheme();
  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium ${isDark ? 'bg-white/10 text-gray-300' : 'bg-black/5 text-gray-700'}`}>
      <Icon className="w-3.5 h-3.5" />
      {label}
    </span>
  );
};

const PromptShowcase = () => {
  const { t } = useTranslation();
  const { isDark } = useTheme();

  return (
    <section className="py-20 relative px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold mb-4">{t('prompt_showcase_title') || 'Prompt Case Study'}</h2>
        <p className={`max-w-2xl mx-auto ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
          {t('prompt_showcase_subtitle') || 'See how we craft prompts for consistent, high-quality AI generations.'}
        </p>
      </div>

      <div className="max-w-4xl mx-auto relative group">
        {/* Animated Glowing Border Layer */}
        <div className="absolute -inset-[2px] rounded-[30px] overflow-hidden opacity-0 group-hover:opacity-100 transition-opacity duration-500 z-0 pointer-events-none">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[200%] h-[200%] animate-[spin_3s_linear_infinite] bg-[conic-gradient(from_0deg,transparent_60%,rgba(220,38,38,0.8)_80%,rgba(99,102,241,0.8)_100%)]"></div>
        </div>

        {/* Actual Card Content */}
        <div className={`relative z-10 w-full h-full rounded-[28px] overflow-hidden transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${isDark ? 'bg-[#1E1F20]' : 'bg-white shadow-xl'}`}>
        {/* Top Row: Visuals */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
            {/* References Column */}
            <div className="flex flex-col gap-4">
              <div className={`relative aspect-[3/4] rounded-2xl overflow-hidden ${isDark ? 'bg-[#131314]' : 'bg-[#E8ECF1]'} border ${isDark ? 'border-white/5' : 'border-black/5'} group`}>
                <img src="/prompt-demo/ref1.jpg" alt="Foto Produk Box (Reference 1)" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent pointer-events-none"></div>
                <div className="absolute bottom-3 left-3 right-3 text-xs font-medium text-white/90">
                  📸 Referensi 1 (Input)
                </div>
              </div>
              <div className={`relative aspect-[3/4] rounded-2xl overflow-hidden ${isDark ? 'bg-[#131314]' : 'bg-[#E8ECF1]'} border ${isDark ? 'border-white/5' : 'border-black/5'} group`}>
                <img src="/prompt-demo/ref2.jpg" alt="Foto Worn (Reference 2)" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent pointer-events-none"></div>
                <div className="absolute bottom-3 left-3 right-3 text-xs font-medium text-white/90">
                  📸 Referensi 2 (Style)
                </div>
              </div>
            </div>

            {/* Result Column */}
            <div className={`relative h-full min-h-[300px] md:min-h-0 rounded-2xl overflow-hidden ${isDark ? 'bg-[#131314]' : 'bg-[#E8ECF1]'} border ${isDark ? 'border-white/5' : 'border-black/5'} group`}>
              <video 
                src="/prompt-demo/result-video.mp4" 
                poster="/prompt-demo/result-thumb.jpg"
                autoPlay 
                loop 
                muted 
                playsInline
                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" 
              />
              <div className="absolute inset-0 bg-black/30 group-hover:bg-black/10 transition-colors pointer-events-none"></div>
              
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="mt-auto mb-4 text-sm font-bold text-white drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)]">
                  🎬 AI Generated Result
                </span>
              </div>
            </div>
        </div>

        {/* Bottom Section: Prompt Text & Badges */}
        <div className={`p-8 border-t ${isDark ? 'border-white/5' : 'border-black/5'}`}>
          <div className="flex flex-wrap gap-2 mb-6">
             <Badge icon={Type} label="UGC Product Review" />
             <Badge icon={Sparkles} label="Omni Flash" />
             <Badge icon={Clock} label="10s" />
             <Badge icon={Play} label="9:16 Portrait" />
             <Badge icon={Globe} label="Indonesian" />
          </div>

          <div className="relative">
            <p className={`font-mono text-sm leading-relaxed ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
              ACTION: Begin at 0.0s with an energetic subtle upper-body lean-in toward the camera while opening the product box on the table with animated, natural hand gestures and direct engaging eye contact, revealing the exact referenced product and presenting it forward...
            </p>
            <p className={`font-mono text-sm leading-relaxed mt-2 filter blur-sm select-none ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              The background should be a modern minimalist living room with warm lighting. Maintain consistent lighting on the subject's face. End the sequence with a smooth zoom out while the subject points to the product...
            </p>
            <p className={`font-mono text-sm leading-relaxed mt-2 filter blur-md select-none ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              Camera angles must shift precisely on the beat, showing high definition textures of the product...
            </p>
            
            {/* Blur Overlay & CTA */}
            <div className={`absolute inset-0 flex flex-col items-center justify-end pb-4 z-10 ${isDark ? 'bg-gradient-to-t from-[#1E1F20] via-[#1E1F20]/80 to-transparent' : 'bg-gradient-to-t from-white via-white/80 to-transparent'}`}>
              <button className="flex items-center gap-2 px-6 py-3 rounded-full bg-crimson-600 hover:bg-crimson-700 text-white font-medium shadow-lg hover:-translate-y-1 transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)]">
                <Lock className="w-4 h-4" />
                Unlock Full Prompt — $2
              </button>
            </div>
          </div>
        </div>
        </div>
      </div>
    </section>
  );
};

export default PromptShowcase;
