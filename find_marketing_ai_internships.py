#!/usr/bin/env python3
"""
Find the most suitable internships for Summer 2026 for a PhD in Marketing, Human-AI Interaction.
"""

import pandas as pd
import re

def calculate_relevance_score(position, company, location):
    """
    Calculate relevance score based on keywords related to Marketing, Human-AI Interaction.
    Higher score = more relevant.
    """
    score = 0
    
    # Convert to lowercase for case-insensitive matching
    position_lower = position.lower()
    company_lower = company.lower()
    
    # CRITICAL matches for Marketing/Human-AI Interaction (weight: 10)
    critical_keywords = [
        'product strategy', 'product management', 'product intern', 'ai product',
        'growth', 'marketing', 'business development', 'user experience', 'ux',
        'content creation', 'consumer', 'customer', 'behavior'
    ]
    
    # Highly relevant keywords (weight: 6)
    high_relevance_keywords = [
        'product', 'strategy', 'interaction', 'user', 'human', 'nlp',
        'content', 'experience', 'generative ai', 'generative'
    ]
    
    # Moderately relevant keywords (weight: 4)
    moderate_relevance_keywords = [
        'research', 'researcher', 'research scientist', 'applied scientist',
        'machine learning', 'ml', 'llm', 'ai research'
    ]
    
    # Lower relevance (but still relevant) keywords (weight: 2)
    low_relevance_keywords = [
        'data science', 'data scientist', 'engineer', 'intern'
    ]
    
    # Check for Summer 2026 specifically (weight: 8)
    if 'summer 2026' in position_lower or 'summer intern 2026' in position_lower:
        score += 8
    elif '2026' in position_lower:
        score += 3
    
    # Check for PhD-specific roles (weight: 5)
    if 'phd' in position_lower:
        score += 5
    
    # Check critical keywords first
    for keyword in critical_keywords:
        if keyword in position_lower:
            score += 10
            break  # Only count once to avoid double counting
    
    # Check high relevance keywords
    for keyword in high_relevance_keywords:
        if keyword in position_lower:
            score += 6
    
    # Check moderate relevance keywords
    for keyword in moderate_relevance_keywords:
        if keyword in position_lower:
            score += 4
    
    # Check low relevance keywords
    for keyword in low_relevance_keywords:
        if keyword in position_lower:
            score += 2
    
    # Bonus for combinations that indicate human-AI interaction focus
    if ('research' in position_lower or 'research intern' in position_lower) and \
       ('generative' in position_lower or 'llm' in position_lower or 'nlp' in position_lower):
        score += 8
    
    if 'product' in position_lower and ('ai' in position_lower or 'generative' in position_lower):
        score += 10
    
    # Penalize pure quantitative trading roles (not relevant for marketing)
    if any(term in position_lower for term in ['quantitative trading', 'quant trader', 'quantitative developer']):
        score -= 15
    
    return max(0, score)  # Ensure score is non-negative

def filter_summer_2026(df):
    """Filter for Summer 2026 internships or general 2026 internships."""
    # Filter for Summer 2026, 2026, or positions that might be summer (most internships are summer)
    # Also include positions without specific dates if they're highly relevant
    mask = (
        df['Position'].str.contains('Summer 2026', case=False, na=False) |
        df['Position'].str.contains('Summer Intern 2026', case=False, na=False) |
        df['Position'].str.contains('2026', case=False, na=False) |
        df['Position'].str.contains('Summer', case=False, na=False)
    )
    return df[mask].copy()

def main():
    # Read the CSV file
    print("Loading internship data...")
    df = pd.read_csv('/workspace/AI_Internships_2026.csv')
    
    print(f"Total internships in dataset: {len(df)}")
    
    # Filter for Summer 2026
    summer_2026 = filter_summer_2026(df)
    print(f"Summer 2026 internships: {len(summer_2026)}")
    
    # Calculate relevance scores
    summer_2026['Relevance Score'] = summer_2026.apply(
        lambda row: calculate_relevance_score(row['Position'], row['Company'], row['Location']),
        axis=1
    )
    
    # Sort by relevance score (descending) and then by age (ascending - newer postings first)
    summer_2026['Age (days)'] = pd.to_numeric(summer_2026['Age (days)'], errors='coerce').fillna(999)
    summer_2026 = summer_2026.sort_values(
        by=['Relevance Score', 'Age (days)'], 
        ascending=[False, True]
    )
    
    # Filter for top relevant ones (score >= 15 for marketing/human-AI focus)
    top_internships = summer_2026[summer_2026['Relevance Score'] >= 15].copy()
    
    print("\n" + "="*80)
    print("MOST SUITABLE INTERNSHIPS FOR PhD IN MARKETING, HUMAN-AI INTERACTION")
    print("="*80 + "\n")
    
    if len(top_internships) > 0:
        # Display top 25 most relevant
        display_count = min(25, len(top_internships))
        
        for idx, row in top_internships.head(display_count).iterrows():
            print(f"Rank: {idx + 1} | Relevance Score: {row['Relevance Score']:.0f}")
            print(f"Company: {row['Company']}")
            print(f"Position: {row['Position']}")
            print(f"Location: {row['Location']}")
            if pd.notna(row['Salary']) and row['Salary']:
                print(f"Salary: {row['Salary']}")
            if pd.notna(row['Application URL']) and row['Application URL']:
                print(f"Application: {row['Application URL']}")
            print(f"Company Website: {row['Company URL']}")
            if pd.notna(row['Age (days)']):
                print(f"Posted: {int(row['Age (days)'])} days ago")
            print("-" * 80)
        
        print(f"\nTotal suitable internships found: {len(top_internships)}")
        print(f"Showing top {display_count} results.")
        
        # Save to CSV
        output_file = '/workspace/Marketing_AI_Internships_Summer_2026.csv'
        top_internships.to_csv(output_file, index=False)
        print(f"\n✓ Results saved to: {output_file}")
    else:
        print("No highly relevant internships found with score >= 15.")
        print("\nShowing top 20 Summer 2026 internships sorted by relevance:\n")
        for idx, row in summer_2026.head(20).iterrows():
            print(f"Score: {row['Relevance Score']:.0f} | {row['Company']} - {row['Position']}")
    
    # Additional insights
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print(f"Total Summer 2026 internships: {len(summer_2026)}")
    print(f"Highly relevant (score >= 15): {len(top_internships)}")
    print(f"Average relevance score: {summer_2026['Relevance Score'].mean():.2f}")
    print(f"Max relevance score: {summer_2026['Relevance Score'].max():.0f}")
    
    # Show breakdown by region
    print("\nBy Region:")
    print(summer_2026['Region'].value_counts())
    
    # Show top companies
    print("\nTop Companies (by relevance):")
    company_scores = top_internships.groupby('Company')['Relevance Score'].mean().sort_values(ascending=False).head(10)
    for company, score in company_scores.items():
        count = top_internships[top_internships['Company'] == company].shape[0]
        print(f"  {company}: {score:.1f} avg score ({count} positions)")

if __name__ == '__main__':
    main()
