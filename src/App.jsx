import React, { useState, useEffect } from 'react';
import { ThemeProvider } from './components/ThemeProvider';
import { I18nProvider } from './i18n.jsx';
import Layout from './components/Layout';
import HeroSection from './components/HeroSection';
import ProductCatalog from './components/ProductCatalog';
import PromptShowcase from './components/PromptShowcase';
import PromptShowcasePage from './components/PromptShowcasePage';

export default function App() {
  const [page, setPage] = useState(window.location.hash);

  useEffect(() => {
    const onHashChange = () => setPage(window.location.hash);
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  const isShowcase = page === '#/showcase';

  return (
    <I18nProvider>
      <ThemeProvider>
        <Layout hideNav={false}>
          {isShowcase ? (
            <PromptShowcasePage />
          ) : (
            <>
              <HeroSection />
              <ProductCatalog />
              <PromptShowcase />
            </>
          )}
        </Layout>
      </ThemeProvider>
    </I18nProvider>
  );
}
