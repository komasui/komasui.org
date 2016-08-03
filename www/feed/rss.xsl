<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:rss="http://purl.org/rss/1.0/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  exclude-result-prefixes="rdf rss dc content"
>

<xsl:template match="/">
  <xsl:apply-templates select="rdf:RDF"/>
</xsl:template>

<xsl:template match="rdf:RDF">
<html xml:lang="ja" lang="ja">
<head>
  <title><xsl:value-of select="rss:channel/rss:title"/></title>
  <link rel="alternate" type="application/rss+xml" title="{rss:channel/rss:title}" href="{rss:channel/rss:link}" />
</head>
<body>
<h1><a href="{rss:channel/rss:link}"><xsl:value-of select="rss:channel/rss:title"/></a></h1>

<p>
  <a href="{rss:channel/rss:link}"><xsl:value-of select="rss:channel/rss:title"/></a>は全<xsl:value-of select="count(rss:item)"/>件あります。
  RSSフィードをXSL変換して表示しています。<br />
  このRSSフィードをお使いのRSSリーダーに登録すれば<a href="{rss:channel/rss:link}"><xsl:value-of select="rss:channel/rss:title"/></a>のRSSを購読できます。
</p>

<ul>
<xsl:apply-templates select="rss:item"/>
</ul>

<p><a href="{rss:channel/rss:link}">狛江市民吹奏楽団</a></p>

</body>
</html>
</xsl:template>

<xsl:template match="rss:item">
  <li><a href="{rss:link}"><xsl:value-of select="substring(dc:date, 1, 10)" /></a>：<xsl:value-of select="rss:description"/></li>
</xsl:template>

</xsl:stylesheet>
