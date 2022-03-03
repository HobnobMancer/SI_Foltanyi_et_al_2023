# imports
knitr::opts_chunk$set(echo = TRUE, warning = FALSE, message = FALSE)
library('kableExtra')
library(data.table)
library('ggplot2')
library("dplyr")
library("GGally")
library(knitr)
library(tidyverse)
library(RColorBrewer)
library(cowplot)
library(viridis)
library(plotly)
library(Rcpp)
library(bio3d)
library(imager)

# Import data files
blastp_results <- read.csv("results/blastp_gh3_complex_proteins.tsv", header=FALSE, sep="\t")

# change column names
setnames(
  blastp_results,
  old = c('V1','V2','V3','V4','V5','V6','V7','V8','V9'),
  new = c('qseqid','sseqid','pident','cov','qlen','slen','alen','bitscore','evalue')
)
# 
# # plot interactive heatmap and save to HTML file
# data <- blastp_results %>%
#   mutate(text = paste("Query seq ID: ", query.seq.id, "\n", "Subject seq ID: ", subject.seq.id, "\n", "Identity(%): ", round(pident,3)))
# 
# p.interactive <- ggplot(data, aes(query.seq.id, subject.seq.id, fill= BSR, text=text)) + 
#   geom_tile() +
#   scale_fill_viridis(limits = c(0.8, 2.05), oob = scales::squish) +
#   xlab("Query seq ID") + 
#   ylab("Subject seq ID") +
#   theme(axis.text.x = element_text(angle=90, vjust=.5, hjust=1))
# p.interactive <- ggplotly(p, tooltip="text")


# plot heatmap and save to pdf and svg
p.static <- ggplot(blastp_results, aes(qseqid, sseqid, fill= pident)) + 
  geom_tile() +
  scale_fill_viridis(discrete=FALSE) +
  xlab("Query seq ID") + 
  ylab("Subject seq ID") +
  theme(axis.text.x = element_text(angle=90, vjust=.5, hjust=1))
p.static

pdf(file = "blastpGh3ComplexProteins.pdf", width = 8, height = 8)
p.static
dev.off()

svg(file = "blastpGh3ComplexProteins.svg", width = 8, height = 8)
p.static
dev.off()