#!/usr/bin/env python3
"""
Detailed analysis of internships specifically matching Marketing + Human-AI Interaction PhD.
"""

import pandas as pd

def main():
    # Read the CSV file
    df = pd.read_csv('/workspace/AI_Internships_2026.csv')
    
    # Key search terms for Marketing + Human-AI Interaction
    marketing_keywords = [
        'product strategy', 'product management', 'growth', 'marketing',
        'business development', 'content creation', 'consumer', 'customer'
    ]
    
    human_ai_keywords = [
        'nlp', 'llm', 'generative ai', 'generative', 'content creation',
        'human', 'interaction', 'user experience', 'ux', 'product intern'
    ]
    
    # Filter positions
    position_lower = df['Position'].str.lower()
    
    # Find highly relevant positions
    highly_relevant = []
    
    for idx, row in df.iterrows():
        pos = row['Position'].lower()
        score = 0
        reasons = []
        
        # Check for marketing-related terms
        for keyword in marketing_keywords:
            if keyword in pos:
                score += 10
                reasons.append(f"Marketing: {keyword}")
        
        # Check for human-AI interaction terms
        for keyword in human_ai_keywords:
            if keyword in pos:
                score += 10
                reasons.append(f"Human-AI: {keyword}")
        
        # Check for research (good for PhD)
        if 'research' in pos or 'researcher' in pos:
            score += 5
            reasons.append("Research role")
        
        # Check for PhD requirement
        if 'phd' in pos:
            score += 5
            reasons.append("PhD required")
        
        # Check for Summer 2026
        if 'summer 2026' in pos or '2026' in pos:
            score += 3
            reasons.append("Summer 2026")
        
        # Penalize pure quant trading roles
        if any(x in pos for x in ['quantitative trading', 'quant trader']):
            score -= 20
        
        if score >= 15:
            highly_relevant.append({
                'Score': score,
                'Company': row['Company'],
                'Position': row['Position'],
                'Location': row['Location'],
                'Salary': row['Salary'] if pd.notna(row['Salary']) and row['Salary'] else 'Not specified',
                'Application URL': row['Application URL'] if pd.notna(row['Application URL']) and row['Application URL'] else 'Check company website',
                'Company URL': row['Company URL'],
                'Region': row['Region'],
                'Age (days)': int(row['Age (days)']) if pd.notna(row['Age (days)']) and row['Age (days)'] != '' else 'Unknown',
                'Reasons': ' | '.join(set(reasons))
            })
    
    # Sort by score
    highly_relevant.sort(key=lambda x: x['Score'], reverse=True)
    
    # Print results
    print("=" * 100)
    print("MOST SUITABLE INTERNSHIPS FOR PhD IN MARKETING, HUMAN-AI INTERACTION - DETAILED ANALYSIS")
    print("=" * 100)
    print(f"\nFound {len(highly_relevant)} highly relevant positions\n")
    
    for i, item in enumerate(highly_relevant, 1):
        print(f"\n{'='*100}")
        print(f"#{i} - RELEVANCE SCORE: {item['Score']}")
        print(f"{'='*100}")
        print(f"Company: {item['Company']}")
        print(f"Position: {item['Position']}")
        print(f"Location: {item['Location']}")
        print(f"Region: {item['Region']}")
        print(f"Salary: {item['Salary']}")
        print(f"Application: {item['Application URL']}")
        print(f"Company Website: {item['Company URL']}")
        print(f"Posted: {item['Age (days)']} days ago")
        print(f"\nWhy it's relevant: {item['Reasons']}")
    
    # Create summary DataFrame and save
    summary_df = pd.DataFrame(highly_relevant)
    output_file = '/workspace/Top_Marketing_AI_Internships_Detailed.csv'
    summary_df.to_csv(output_file, index=False)
    print(f"\n{'='*100}")
    print(f"Summary saved to: {output_file}")
    print(f"Total positions found: {len(highly_relevant)}")
    print(f"{'='*100}")
    
    # Top 5 recommendations
    print("\n" + "=" * 100)
    print("TOP 5 RECOMMENDATIONS:")
    print("=" * 100)
    for i, item in enumerate(highly_relevant[:5], 1):
        print(f"\n{i}. {item['Company']} - {item['Position']}")
        print(f"   Location: {item['Location']}")
        print(f"   Score: {item['Score']} | {item['Reasons']}")

if __name__ == '__main__':
    main()
