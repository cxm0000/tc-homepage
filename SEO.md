# Search and AI discovery

Canonical production homepage: https://tangcai.se/

The homepage is static HTML: company details, app descriptions, and links work without JavaScript. Inline JSON-LD connects the Organization, WebSite, WebPage, app list, and six SoftwareApplication entities. App metadata describes visible content; no prices, ratings, or release availability are invented. Personal details are excluded.

`robots.txt` allows public crawlers and advertises `sitemap.xml`. This also allows training crawlers under the existing unrestricted policy; no bot-specific restrictions are introduced. Robots rules are advisory and do not override CDN/firewall rules.

`llms.txt` is a supplementary plain-text company and product directory. It does not guarantee agent usage or improve Google rankings. Maintain it alongside visible copy and JSON-LD. Google does not require AI-specific markup: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

## Verification

Run `python3 scripts/check-seo.py` from the project root after editing content or URLs. It checks metadata, JSON-LD references, all six product links, image paths, section anchors, sitemap URLs, and robots access.

## Publication

GitHub Pages publishes through `.github/workflows/deploy-pages.yml` on pushes to `main` and manual workflow dispatch. The Pages custom domain is `tangcai.se`.

The build checks source SEO, packages only public files into `_site`, and validates the output before deployment. Canonical URLs use the configured Pages domain and always use HTTPS. GitHub manages the TLS certificate.

Website DNS: apex A/AAAA use GitHub Pages addresses; www is a CNAME to `cxm0000.github.io`. Existing mail records and other services are preserved. The previous CloudFront/S3 resources are retained for rollback; this deployment does not delete them.

After domain or content changes, check HTTPS, metadata, assets, robots, and sitemap on the live domain. Run `python3 scripts/check-seo.py` locally. Validate structured data with Schema.org Validator, submit `https://tangcai.se/sitemap.xml` to existing verified Search Console/Bing properties, and measure production Core Web Vitals. Publication does not guarantee indexing or AI citations.
