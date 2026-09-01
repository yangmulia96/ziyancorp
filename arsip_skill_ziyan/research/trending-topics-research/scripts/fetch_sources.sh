#!/usr/bin/env bash
# Fetch trending sources for Compound Daily research into a FRESH daily dir.
# Avoids: /tmp (forbidden), absolute -o exit 23 (use cd + relative -o),
# and & backgrounding (forbidden in terminal foreground) -> sequential with ';'.
set -u
DIR="/c/Users/arija/research_$(date +%F)"
mkdir -p "$DIR"
cd "$DIR" || exit 1
UA="Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
curl -sS "https://news.google.com/rss/search?q=AI+when:2d&hl=en-US&gl=US&ceid=US:en" -o gn_ai.xml
curl -sS "https://news.google.com/rss/search?q=finance+when:2d&hl=en-US&gl=US&ceid=US:en" -o gn_fin.xml
curl -sS "https://news.google.com/rss/search?q=technology+when:2d&hl=en-US&gl=US&ceid=US:en" -o gn_tech.xml
curl -sS "https://news.google.com/rss/search?q=stock+market+when:2d&hl=en-US&gl=US&ceid=US:en" -o gn_stock.xml
curl -sS "https://news.google.com/rss/search?q=semiconductor+when:2d&hl=en-US&gl=US&ceid=US:en" -o gn_semi.xml
curl -sS -A "$UA" "https://techcrunch.com/feed/" -o tc.xml
curl -sS "https://arstechnica.com/feed/" -o at.xml
echo "Fetched to $DIR"
ls -la gn_*.xml tc.xml at.xml
