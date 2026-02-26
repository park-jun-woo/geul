HUGO := /home/parkjunwoo/bin/hugo
INDEXNOW_KEY := # TODO: generate key
DOMAIN := https://geul.org

.PHONY: serve build clean deploy indexnow

serve:
	$(HUGO) server -D

build:
	$(HUGO) --minify

clean:
	rm -rf public/

deploy: build
	aws s3 sync public/ s3://geul-org-public/ --delete --exact-timestamps
	aws s3 cp s3://geul-org-public/ s3://geul-org-public/ --recursive --exclude "*" --include "*.xml" --content-type "application/xml; charset=utf-8" --metadata-directive REPLACE
	aws cloudfront create-invalidation --distribution-id $(CF_DIST_ID) --paths "/*"
	@$(MAKE) indexnow

indexnow:
	@echo "Submitting URLs to IndexNow..."
	@URLS=$$(grep -oP '(?<=<loc>)[^<]+' public/sitemap.xml 2>/dev/null); \
	if [ -z "$$URLS" ]; then echo "No URLs found in sitemap.xml"; exit 0; fi; \
	URL_LIST=$$(echo "$$URLS" | head -10000 | sed 's/.*/"&"/' | paste -sd, | sed 's/^/[/;s/$$/]/'); \
	curl -s -X POST "https://api.indexnow.org/indexnow" \
		-H "Content-Type: application/json" \
		-d "{\"host\":\"geul.org\",\"key\":\"$(INDEXNOW_KEY)\",\"keyLocation\":\"$(DOMAIN)/$(INDEXNOW_KEY).txt\",\"urlList\":$$URL_LIST}" \
		-w "\nHTTP %{http_code}\n"; \
	echo "Done."
