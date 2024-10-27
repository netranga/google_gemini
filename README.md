# CS229 Machine Learning Course Assistant using Gemini AI

## Overview
This project creates an intelligent course assistant for Stanford's CS229 "Introduction to Machine Learning" course using Google's Gemini AI model. It leverages Gemini's long context windows to process and provide insights on an entire semester's worth of course content. This project is part of a Kaggle competition focused on innovative applications of large context window AI models.

## Key Features

1. **Comprehensive Course Material Integration**
   - Lecture transcripts from YouTube videos: Used Youtube Data API to pull transcripts of Fall 2022 lecture playlist (https://www.youtube.com/playlist?list=PLoROMvodv4rNyWOpJg_Yh4NSqI4Z4vOYy)
   - PowerPoint slides (regular and annotated versions): Pulled from the CS229 course website (https://docs.google.com/spreadsheets/d/18pHRegyB0XawIdbZbvkr8-jMfi_2ltHVYPjBEOim-6w/edit?pli=1&gid=0#gid=0)
   - Course textbook content: Pulled from the CS229 course website

2. **Knowledge Cache**
   - 1M tokens of cached knowledge for free Gemini users
   - Can upload entire semester's worth of lecture transcripts and slides
   - Different cuts of information can be incorporated into different caches

3. **Information Retrieval**
Various types of questions can be asked across entire semester's worth of content
   - Lecture-specific questions (missed a lecture and looking to summarize, compare content between lecture and in notes)
   - Exam preparation assistance (using midterm review session and textboo content to generate additional practice problems)
   - Comparison between annotated and regular notes
   - Cross-lecture concept connections (connecting concepts across different lectures)


## Why This Idea?

1. **Maximizes Gemini's Long Context Window Capability**: Fully utilizes Gemini's extensive context window, allowing for comprehensive analysis of an entire semester's worth of machine learning course content

2. **Multi-dimensional Information Retrieval**: Enables students to access and cross-reference information from various sources (lectures, slides, textbooks) and perspectives (annotated vs. regular notes). If a student is looking for a quick summary of a concept, they can get a summary of the concept from the lecture transcript, see the concept in the annotated slides, and see an example of the concept in the textbook. Questions can be asked at varying levels of granularity depending on the student's needs.


## Setup and Usage

[Add instructions for setting up and using the project, including any required API keys or dependencies]

## Future Improvements

[List any planned enhancements or areas for future development]

## Kaggle Competition

This project is an entry in a Kaggle competition focused on identifying beneficial use cases for AI models with large context windows. It demonstrates the potential of such models in educational applications, particularly for processing and retrieving information from extensive course materials.
