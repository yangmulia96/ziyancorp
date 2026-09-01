import React from 'react';
import { useTranslation } from '../i18n.jsx';
import { ArrowRight, ExternalLink, Sparkles, BookOpen, Gift, Flame } from 'lucide-react';
import { useTheme } from './ThemeProvider';
import productsData from '../data/products.json';

const ProductCatalog = () => {
  const { t } = useTranslation();
  const { isDark } = useTheme();

  return (
    <section id="products" className="py-20 relative px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold tracking-wider uppercase mb-4 border border-crimson-500/30 bg-crimson-500/10 text-crimson-400">
            <Flame className="w-3.5 h-3.5 text-crimson-500" />
            <span>Official Store • Lynk.id @yang_mulia</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold mb-4 tracking-tight">
            {t('catalog_title') || 'Katalog Produk Digital'}
          </h2>
          <p className={"max-w-2xl mx-auto text-base sm:text-lg " + (isDark ? 'text-gray-400' : 'text-gray-600')}>
            Aset digital siap pakai, panduan automasi, dan database formula konten viral. Transaksi otomatis & instan via Lynk.id.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {productsData.map((product) => {
            const isFree = product.is_free;
            
            return (
              <div key={product.id} className="relative group rounded-[32px] p-[2px] transition-all duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] hover:-translate-y-2 flex flex-col">
                {/* 1. Spectral Volumetric Light — Ambient Continuous Aura */}
                <div className={"absolute -inset-1 rounded-[34px] bg-gradient-to-r " + (product.border_glow || "from-crimson-600 via-violet-600 to-cyan-500") + " blur-xl opacity-30 group-hover:opacity-90 transition-opacity duration-700 pointer-events-none animate-pulse"}></div>

                {/* 2. Luminous Glow Perimeter — Rotating Spectral Conic Gradient */}
                <div className="absolute inset-0 rounded-[32px] overflow-hidden pointer-events-none">
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[250%] h-[250%] animate-[spin_6s_linear_infinite] opacity-50 group-hover:opacity-100 transition-opacity duration-500 bg-[conic-gradient(from_0deg,#DC2626_0%,#8B5CF6_30%,#06B6D4_60%,#F43F5E_85%,#DC2626_100%)]"></div>
                </div>

                {/* 3. Card Core — Glassmorphism & Tonal Surface */}
                <div className={"relative z-10 h-full p-6 sm:p-7 rounded-[30px] flex flex-col backdrop-blur-xl transition-colors duration-300 " + (isDark ? 'bg-[#1E1F20]/95 border border-white/10' : 'bg-white/95 border border-black/5 shadow-2xl')}>
                  
                  {/* Product Thumbnail & Badge */}
                  <div className="relative mb-6 rounded-2xl overflow-hidden aspect-[4/5] bg-black/20 border border-white/10 group-hover:scale-[1.02] transition-transform duration-500">
                    {product.image ? (
                      <img 
                        src={product.image} 
                        alt={product.title}
                        className="w-full h-full object-cover object-top"
                        loading="lazy"
                      />
                    ) : (
                      <div className={"w-full h-full flex items-center justify-center bg-gradient-to-br " + product.color}>
                        <Sparkles className="w-12 h-12 text-white/80" />
                      </div>
                    )}

                    {/* Luminous Floating Badge */}
                    <div className="absolute top-3 right-3">
                      <span className={"inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold text-white shadow-lg backdrop-blur-md border border-white/20 " + (isFree ? 'bg-emerald-600/90' : 'bg-crimson-600/90')}>
                        {isFree ? <Gift className="w-3 h-3" /> : <Sparkles className="w-3 h-3" />}
                        {product.badge || (isFree ? 'GRATIS' : 'PREMIUM')}
                      </span>
                    </div>
                  </div>
                  
                  {/* Title & Description */}
                  <h3 className="text-xl font-bold mb-3 tracking-tight leading-snug group-hover:text-crimson-400 transition-colors">
                    {product.title}
                  </h3>
                  <p className={"mb-6 flex-grow text-sm leading-relaxed " + (isDark ? 'text-gray-300' : 'text-gray-600')}>
                    {product.description}
                  </p>

                  {/* Price & Direct Lynk.id Action Button */}
                  <div className="flex items-center justify-between mt-auto pt-5 border-t border-gray-500/15 gap-4">
                    <div>
                      <span className="block text-[11px] uppercase tracking-wider text-gray-400 font-semibold">Harga</span>
                      <span className={"font-bold text-xl tracking-tight " + (isFree ? 'text-emerald-400' : 'text-white')}>
                        {product.price}
                      </span>
                    </div>

                    <a 
                      href={product.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={"relative group/btn inline-flex items-center gap-1.5 text-sm font-semibold px-5 py-2.5 rounded-full text-white shadow-lg transition-all duration-300 hover:scale-105 " + (isFree ? 'bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 shadow-emerald-900/40' : 'bg-gradient-to-r from-crimson-600 to-rose-600 hover:from-crimson-500 hover:to-rose-500 shadow-crimson-900/40')}
                    >
                      <span>{product.btn_label || (isFree ? 'Ambil Gratis' : 'Beli Sekarang')}</span>
                      <ExternalLink className="w-3.5 h-3.5 group-hover/btn:translate-x-0.5 group-hover/btn:-translate-y-0.5 transition-transform" />
                    </a>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* View All on Lynk.id Footer CTA */}
        <div className="mt-16 text-center">
          <a
            href="https://lynk.id/yang_mulia"
            target="_blank"
            rel="noopener noreferrer"
            className={"inline-flex items-center gap-2.5 px-7 py-3 rounded-full text-sm font-semibold backdrop-blur-xl border transition-all duration-300 hover:scale-105 " + (isDark ? 'bg-white/5 border-white/10 hover:bg-white/10 text-white' : 'bg-black/5 border-black/10 hover:bg-black/10 text-black')}
          >
            <span>Kunjungi Toko Lengkap di Lynk.id (@yang_mulia)</span>
            <ArrowRight className="w-4 h-4 text-crimson-500" />
          </a>
        </div>
      </div>
    </section>
  );
};

export default ProductCatalog;
