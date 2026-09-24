# Search and AI discovery

Canonical production homepage: https://tangcai.se/

The homepage is static HTML: company details, app descriptions, and links work without JavaScript. Inline JSON-LD connects the Organization, WebSite, WebPage, app list, and six SoftwareApplication entities. App metadata describes visible content; no prices, ratings, or release availability are invented. The company homepage avoids personal details; the consulting page uses the approved first name Xiaoming and company email.

`robots.txt` allows public crawlers and advertises `sitemap.xml`. This also allows training crawlers under the existing unrestricted policy; no bot-specific restrictions are introduced. Robots rules are advisory and do not override CDN/firewall rules.

`llms.txt` is a supplementary plain-text company and product directory. It does not guarantee agent usage or improve Google rankings. Maintain it alongside visible copy and JSON-LD. Google does not require AI-specific markup: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

## Verification

Run `python3 scripts/check-seo.py` from the project root after editing content or URLs. It checks metadata, JSON-LD references, all six product links, image paths, section anchors, sitemap URLs, and robots access.

## Publication

GitHub Pages publishes through `.github/workflows/deploy-pages.yml` on pushes to `main` and manual workflow dispatch. The Pages custom domain is `tangcai.se`.

The build checks source SEO, packages only public files into `_site`, and validates the output before deployment. Canonical URLs use the configured Pages domain and always use HTTPS. GitHub manages the TLS certificate.

Website DNS: apex A/AAAA use GitHub Pages addresses; www is a CNAME to `cxm0000.github.io`. Existing mail records and other services are preserved. The previous CloudFront/S3 resources are retained for rollback; this deployment does not delete them.

After domain or content changes, check HTTPS, metadata, assets, robots, and sitemap on the live domain. Run `python3 scripts/check-seo.py` locally. Validate structured data with Schema.org Validator, submit `https://tangcai.se/sitemap.xml` to existing verified Search Console/Bing properties, and measure production Core Web Vitals. Publication does not guarantee indexing or AI citations.

## AI workflow consulting page

Canonical: https://tangcai.se/work-with-me/

The title and visible copy describe AI workflow consulting for small businesses. The page has one H1, a descriptive homepage link, visible breadcrumbs, social metadata, and a sitemap entry. JSON-LD connects WebPage, Service, Person, Organization, WebSite, and BreadcrumbList through stable identifiers. WebPage reflects the primary service offer. No unsupported credentials, prices, ratings, savings, locations, or client results are included.

Visible questions and answers explain scope, example tasks, pricing approach, evaluation, and contact in static HTML. No FAQ rich-result eligibility is claimed. The supplementary llms.txt links to the service and answers; it does not guarantee AI usage or citations.

The checker validates entity references, social metadata, crawler access, internal anchors, portfolio links, and packaged output. After publication, verify the live page returns 200 with its intended canonical, then request indexing through existing verified search-console properties. Indexing, rankings, traffic, and AI mentions remain unverified until observed in production.

Reference: https://developers.google.com/search/docs/appearance/ai-features

## FDE positioning and career evidence

The service page now includes a Forward Deployed Engineering (FDE) approach, while keeping the workflow pilot as the first engagement. FDE is an offered approach, not a claimed previous job title. The Person entity links to the user-supplied LinkedIn profile through sameAs.

Career themes were checked against https://www.linkedin.com/in/ming83/ on 2026-09-24: software engineering and management, solutions architecture, healthcare digitisation, SaaS, and API management. The About section and headline differ on current organisation, so the page does not assert a current employer or precise tenure. Embedded/wireless experience and income estimates from the supplied analysis are excluded. No employer endorsement is implied.
