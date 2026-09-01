import React, { useState, useRef, useEffect } from 'react';
import { Copy, Check, Play, Pause, ExternalLink, Sparkles, Image, Video, ChevronRight } from 'lucide-react';
import { useTheme } from './ThemeProvider';

const prompt1 = `Create a hyper-realistic commercial product video of a luxury Swiss watch "OPK 8151" on a dark obsidian surface. 
The watch face shows intricate golden details. 
Cinematic lighting with dramatic rim light and soft bokeh background. 
Camera slowly orbits the watch in a 360-degree arc.
8K resolution, photorealistic, luxury brand commercial style.`;

const cases = [
  {
    id: 1,
    category: 'Product Photography',
    tool: 'Gemini Omni Flash',
    title: 'Jam Tangan Mewah — OPK 8151',
    description: 'Dari foto produk biasa menjadi visual iklan mewah berkualitas studio profesional, tanpa kamera mahal.',
    prompt: prompt1,
    refs: [
      { type: 'image', src: '/prompt-demo/ref1.jpg', label: 'Referensi 1' },
      { type: 'image', src: '/prompt-demo/ref2.jpg', label: 'Referensi 2' },
    ],
    results: [
      { type: 'image', src: '/prompt-demo/result-thumb.jpg', label: 'Hasil Foto' },
      { type: 'video', src: '/prompt-demo/result-video.mp4', label: 'Hasil Video' },
    ],
  },
];

const MediaCard = ({ item, label }) => {
  const videoRef = useRef(null);
  const [playing, setPlaying] = useState(false);

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (playing) { videoRef.current.pause(); setPlaying(false); }
    else { videoRef.current.play(); setPlaying(true); }
  };

  if (item.type === 'video') {
    return (
      <div className="relative rounded-2xl overflow-hidden bg-black group cursor-pointer" onClick={togglePlay}>
        <video
          ref={videoRef}
          src={item.src}
          className="w-full h-48 object-cover"
          loop
          muted
          playsInline
        />
        <div className={`absolute inset-0 flex items-center justify-center transition-opacity ${playing ? 'opacity-0 group-hover:opacity-100' : 'opacity-100'}`}>
          <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center">
            {playing ? <Pause className="w-5 h-5 text-white" /> : <Play className="w-5 h-5 text-white fill-white" />}
          </div>
        </div>
        <div className="absolute bottom-2 left-2">
          <span className="text-xs bg-black/60 text-white px-2 py-1 rounded-full backdrop-blur-sm flex items-center gap-1">
            <Video className="w-3 h-3" /> {label}
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="relative rounded-2xl overflow-hidden">
      <img src={item.src} alt={label} className="w-full h-48 object-cover" />
      <div className="absolute bottom-2 left-2">
        <span className="text-xs bg-black/60 text-white px-2 py-1 rounded-full backdrop-blur-sm flex items-center gap-1">
          <Image className="w-3 h-3" /> {label}
        </span>
      </div>
    </div>
  );
};

const PromptBox = ({ prompt }) => {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(prompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <div className="relative rounded-2xl bg-black/40 border border-white/10 p-4 font-mono text-sm text-green-400 leading-relaxed">
      <button onClick={copy} className="absolute top-3 right-3 p-1.5 rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
        {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4 text-white/60" />}
      </button>
      <pre className="whitespace-pre-wrap pr-8">{prompt}</pre>
    </div>
  );
};

const PromptShowcasePage = () => {
  const { isDark } = useTheme();
  const [activeCase, setActiveCase] = useState(0);
  const [activeTab, setActiveTab] = useState('result');
  const mouseRef = useRef({ x: 0, y: 0 });
  const spotlightRef = useRef(null);

  useEffect(() => {
    const handleMove = (e) => {
      if (!spotlightRef.current) return;
      spotlightRef.current.style.background = `radial-gradient(600px circle at ${e.clientX}px ${e.clientY}px, rgba(220,38,38,0.06), transparent 60%)`;
    };
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  const current = cases[activeCase];

  return (
    <div className={`min-h-screen relative ${isDark ? 'bg-[#131314] text-white' : 'bg-[#F0F4F9] text-gray-900'}`}>
      {/* Cursor spotlight */}
      <div ref={spotlightRef} className="pointer-events-none fixed inset-0 z-10 transition-all duration-100" />

      {/* Header */}
      <div className="relative z-20 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-8">
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-6">
          <a href="/" className="hover:text-crimson-500 transition-colors">ZiyanCorp</a>
          <ChevronRight className="w-4 h-4" />
          <span>Prompt Showcase</span>
        </div>

        <div className="flex items-start gap-4 mb-4">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center text-white shadow-lg flex-shrink-0">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold mb-2">Prompt Showcase</h1>
            <p className={`text-lg ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
              Lihat sendiri kekuatan AI kami — dari referensi, prompt, hingga hasil akhir yang siap jual.
            </p>
          </div>
        </div>
      </div>

      {/* Case Selector */}
      {cases.length > 1 && (
        <div className="relative z-20 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
          <div className="flex gap-3 overflow-x-auto pb-2">
            {cases.map((c, i) => (
              <button
                key={c.id}
                onClick={() => { setActiveCase(i); setActiveTab('result'); }}
                className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-all ${activeCase === i ? 'bg-crimson-600 text-white' : (isDark ? 'bg-white/10 hover:bg-white/20 text-gray-300' : 'bg-black/5 hover:bg-black/10 text-gray-600')}`}
              >
                Case #{c.id} — {c.title}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="relative z-20 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className={`rounded-[28px] overflow-hidden ${isDark ? 'bg-[#1E1F20]' : 'bg-white shadow-xl'}`}>

          {/* Case Header */}
          <div className="p-6 sm:p-8 border-b border-white/10">
            <div className="flex items-center gap-3 flex-wrap">
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-400">{current.category}</span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-400">{current.tool}</span>
            </div>
            <h2 className="text-2xl font-bold mt-3 mb-2">{current.title}</h2>
            <p className={isDark ? 'text-gray-400' : 'text-gray-600'}>{current.description}</p>
          </div>

          {/* Tabs */}
          <div className={`flex border-b ${isDark ? 'border-white/10' : 'border-gray-200'}`}>
            {['ref', 'prompt', 'result'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`flex-1 py-4 text-sm font-medium transition-colors capitalize ${
                  activeTab === tab
                    ? 'text-crimson-500 border-b-2 border-crimson-500'
                    : (isDark ? 'text-gray-500 hover:text-gray-300' : 'text-gray-500 hover:text-gray-700')
                }`}
              >
                {tab === 'ref' ? '📸 Referensi' : tab === 'prompt' ? '💬 Prompt' : '✨ Hasil AI'}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="p-6 sm:p-8">
            {activeTab === 'ref' && (
              <div>
                <p className={`mb-4 text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                  Foto/video referensi yang dikirim sebagai input ke AI.
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {current.refs.map((r, i) => <MediaCard key={i} item={r} label={r.label} />)}
                </div>
              </div>
            )}

            {activeTab === 'prompt' && (
              <div>
                <p className={`mb-4 text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                  Prompt persis yang digunakan — salin dan coba sendiri.
                </p>
                <PromptBox prompt={current.prompt} />
              </div>
            )}

            {activeTab === 'result' && (
              <div>
                <p className={`mb-4 text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                  Hasil yang dihasilkan AI dari referensi + prompt di atas.
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {current.results.map((r, i) => <MediaCard key={i} item={r} label={r.label} />)}
                </div>
              </div>
            )}
          </div>

          {/* CTA */}
          <div className={`mx-6 sm:mx-8 mb-8 p-6 rounded-2xl ${isDark ? 'bg-[#131314]' : 'bg-gray-50'} flex flex-col sm:flex-row items-center justify-between gap-4`}>
            <div>
              <p className="font-semibold mb-1">Mau prompt lengkap seperti ini?</p>
              <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>Dapatkan 25+ master prompt dalam satu paket.</p>
            </div>
            <a href="/#products" className="flex-shrink-0 px-6 py-3 bg-crimson-600 hover:bg-crimson-700 text-white rounded-full font-medium transition-colors flex items-center gap-2">
              Lihat Produk <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PromptShowcasePage;
