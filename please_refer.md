# B2B Lead Generation Platform

## Overview

This is a comprehensive B2B lead generation platform built with Streamlit that helps users find, enrich, and export qualified leads. The platform consists of four main modules: Tech Stack Finder, Email Extractor, Lead Enrichment, and Export functionality. It's designed to help sales teams and business development professionals identify potential customers based on their technology stack and gather actionable contact information.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit with multi-page application structure
- **UI Pattern**: Dashboard-style interface with metrics, forms, and data tables
- **State Management**: Streamlit session state for data persistence across pages
- **Layout**: Wide layout with responsive columns and sidebar navigation

### Backend Architecture
- **Processing Layer**: Utility classes for data processing, web scraping, and enrichment
- **Data Flow**: In-memory processing with pandas DataFrames
- **Session Management**: Streamlit session state handles data persistence during user session

### Data Storage
- **Primary Storage**: In-memory pandas DataFrames stored in Streamlit session state
- **Data Structure**: Structured lead records with columns for company info, contact details, and enrichment data
- **Export Format**: CSV download functionality for lead data

## Key Components

### 1. Tech Stack Finder (`pages/1_Tech_Stack_Finder.py`)
**Purpose**: Discover companies using specific technologies
- **Input**: Technology keywords (React, Shopify, WordPress, etc.)
- **Processing**: Searches GitHub repositories and technology showcases
- **Output**: Company names, domains, and detected tech stacks

### 2. Email Extractor (`pages/2_Email_Extractor.py`)
**Purpose**: Extract and validate professional emails from company websites
- **Input**: Company domains from existing leads or manual entry
- **Processing**: Web scraping, email validation, and professional scoring
- **Output**: Validated emails with quality scores based on role indicators

### 3. Lead Enrichment (`pages/3_Lead_Enrichment.py`)
**Purpose**: Enhance lead data with company information
- **Input**: Company domains and names
- **Processing**: Scrapes public sources for company size, funding status, LinkedIn profiles
- **Output**: Enriched lead profiles with additional business context

### 4. Export Functionality (`pages/4_Export_Leads.py`)
**Purpose**: Download enriched lead data
- **Input**: Processed lead database
- **Processing**: Data formatting and file generation
- **Output**: CSV files ready for CRM import

### 5. Core Utilities
- **DataProcessor**: Centralizes data management and CRUD operations
- **EmailExtractor**: Handles email discovery and validation logic
- **LeadEnrichment**: Manages company data enrichment workflows
- **TechStackFinder**: Implements technology-based company discovery

## Data Flow

1. **Lead Discovery**: Tech Stack Finder identifies companies using target technologies
2. **Contact Extraction**: Email Extractor finds and validates professional contact information
3. **Data Enrichment**: Lead Enrichment adds company context and business intelligence
4. **Export**: Users download qualified leads for outreach campaigns

The platform maintains data consistency through a centralized DataProcessor that handles deduplication and data validation across all modules.

## External Dependencies

### Web Scraping & Data Processing
- **requests**: HTTP client for web scraping
- **beautifulsoup4**: HTML parsing and data extraction
- **trafilatura**: Advanced web content extraction
- **pandas**: Data manipulation and analysis

### Email Processing
- **email-validator**: Email format and domain validation
- **dnspython**: DNS resolution for email verification

### UI Framework
- **streamlit**: Web application framework with built-in components

### Validation Approach
The system uses DNS MX record validation and regex patterns for email verification, avoiding paid API dependencies while maintaining accuracy.

## Deployment Strategy

### Platform
- **Target**: Replit deployment with autoscale configuration
- **Runtime**: Python 3.11 environment
- **Port**: 5000 (configured for Streamlit server)

### Configuration
- Streamlit server configured for headless operation
- Environment optimized for web scraping with appropriate headers
- Session-based data persistence (no external database required)

### Scalability Considerations
- In-memory storage suitable for small to medium datasets
- Stateless design allows for horizontal scaling
- Rate limiting implemented for web scraping to avoid blocks

## Changelog

```
Changelog:
- June 26, 2025: Initial setup and development
- June 26, 2025: Added comprehensive B2B lead generation platform with all modules
- June 26, 2025: Fixed openpyxl dependency for Excel export functionality
- June 26, 2025: Created setup documentation for local laptop deployment
- June 26, 2025: Platform fully functional and ready for SaaSQuatch challenge submission
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```