USE [master]
GO

IF DB_ID('chatbot') IS NOT NULL
  set noexec on               -- prevent creation when already exists

CREATE DATABASE [chatbot];
GO

USE [chatbot]
GO