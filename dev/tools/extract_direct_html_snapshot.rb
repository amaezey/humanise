#!/usr/bin/env ruby
# Extract article-like markdown from downloaded HTML pages when Jina Reader cannot fetch them.

require "cgi"
require "json"

slug, source_url, html_path, out_path = ARGV
abort "usage: extract_direct_html_snapshot.rb SLUG SOURCE_URL HTML_PATH OUT_PATH" unless out_path

html = File.read(html_path, encoding: "UTF-8", invalid: :replace, undef: :replace, replace: "")

def clean_html(text)
  text = text.to_s.dup
  text = CGI.unescapeHTML(text)
  text.gsub!(/<script\b.*?<\/script>/mi, " ")
  text.gsub!(/<style\b.*?<\/style>/mi, " ")
  text.gsub!(/<br\s*\/?>/i, "\n")
  text.gsub!(/<\/p>/i, "\n\n")
  text.gsub!(/<[^>]+>/, " ")
  text.gsub(/\u00a0/, " ")
    .gsub(/[ \t]+/, " ")
    .gsub(/\n[ \t]+/, "\n")
    .gsub(/\n{3,}/, "\n\n")
    .strip
end

def meta_content(html, property)
  if html =~ /<meta[^>]+(?:property|name)=["']#{Regexp.escape(property)}["'][^>]+content=["']([^"']*)["']/i
    CGI.unescapeHTML($1)
  elsif html =~ /<meta[^>]+content=["']([^"']*)["'][^>]+(?:property|name)=["']#{Regexp.escape(property)}["']/i
    CGI.unescapeHTML($1)
  end
end

def ld_json_articles(html)
  flatten = lambda do |value|
    case value
    when Array
      value.flat_map { |item| flatten.call(item) }
    when Hash
      [value] + value.values.flat_map { |item| flatten.call(item) }
    else
      []
    end
  end

  html.scan(%r{<script[^>]+type=["']application/ld\+json["'][^>]*>(.*?)</script>}mi).flat_map do |(raw)|
    begin
      parsed = JSON.parse(raw.strip)
      flatten.call(parsed)
    rescue JSON::ParserError
      begin
        parsed = JSON.parse(CGI.unescapeHTML(raw.strip))
        flatten.call(parsed)
      rescue JSON::ParserError
        []
      end
    end
  end
end

article = ld_json_articles(html).find { |item| item.is_a?(Hash) && item["articleBody"].to_s.strip != "" }
title = article && article["headline"] || meta_content(html, "og:title") || meta_content(html, "twitter:title") || slug
published = article && (article["datePublished"] || article["dateCreated"]) || ""
author = if article && article["author"].is_a?(Hash)
  article["author"]["name"]
elsif article && article["author"].is_a?(Array)
  article["author"].map { |a| a.is_a?(Hash) ? a["name"] : a }.compact.join(", ")
else
  ""
end

body = if article
  article["articleBody"].to_s.strip
else
  paragraphs = html.scan(%r{<p[^>]+class=["'][^"']*slate-paragraph[^"']*["'][^>]*>(.*?)</p>}mi)
                   .map { |(p)| clean_html(p) }
                   .reject(&:empty?)
  if paragraphs.empty?
    article_html =
      if html =~ %r{<section[^>]+class=["'][^"']*body main-article-body[^"']*["'][^>]*>(.*?)(?:<footer\b|</article>)}mi
        $1
      elsif html =~ %r{<div[^>]+class=["'][^"']*post-body[^"']*["'][^>]*>(.*?)(?:<!-- START SUBSCRIBE|</article>)}mi
        $1
      elsif html =~ %r{<article\b[^>]*>(.*?)</article>}mi
        html.scan(%r{<article\b[^>]*>(.*?)</article>}mi).map(&:first).max_by(&:length)
      elsif html =~ %r{<main\b[^>]*>(.*?)</main>}mi
        $1
      end

    if article_html
      article_html = article_html.gsub(%r{<(?:nav|script|style|aside|footer|form|iframe)\b.*?</(?:nav|script|style|aside|footer|form|iframe)>}mi, " ")
      article_html.scan(%r{<(h[1-4]|p|li)[^>]*>(.*?)</\1>}mi)
                  .map { |(_, chunk)| clean_html(chunk) }
                  .reject(&:empty?)
                  .join("\n\n")
    else
      ""
    end
  else
    paragraphs.join("\n\n")
  end
end

abort "no article body extracted from #{html_path}" if body.strip.empty?

content = +"# #{title}\n\n"
content << "- **Source URL:** #{source_url}\n"
content << "- **Snapshot method:** direct HTML article extraction\n"
content << "- **Retrieved:** 2026-05-05\n"
content << "- **Author:** #{author}\n" unless author.to_s.empty?
content << "- **Published:** #{published}\n" unless published.to_s.empty?
content << "\n## Article Body\n\n"
content << clean_html(body)
content << "\n"

File.write(out_path, content)
