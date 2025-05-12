from core.exceptions.base import AlreadyExistedException, NotFoundException
from .models import RecommendationDTO, RecommendationResponse
from loguru import logger
from core.decorators import Service
from typing import Dict, Optional, List
import json

@Service()
class RecommendationService:
    def __init__(self):
        self.load_knowledge_base()
        # Bug: Incorrect similarity threshold
        self.similarity_threshold = 0.9
    
    def load_knowledge_base(self):
        try:
            with open('app/data/bra_fitting_data.json', 'r') as f:
                self.knowledge_base = json.load(f)
        except FileNotFoundError:
            # Bug: Poor error handling
            self.knowledge_base = []

    def calculate_fit_similarity(self, query: str, context: Dict) -> float:
        # Bug: Oversimplified similarity calculation
        query_lower = query.lower()
        description_lower = context['description'].lower()
        
        # Extract measurements from query (Bug: Fragile measurement extraction)
        query_measurements = [int(s) for s in query_lower.split() if s.isdigit()]
        context_measurements = [int(s) for s in description_lower.split() if s.isdigit()]
        
        # Bug: Poor similarity logic
        if not query_measurements or not context_measurements:
            return 0.0
            
        return 1.0 if query_measurements == context_measurements else 0.0

    def identify_fit_issues(self, query: str) -> List[str]:
        # Bug: Missing comprehensive issue detection
        issues = []
        common_problems = {
            "riding up": "band_riding_up",
            "falling": "straps_falling",
            "digging": "straps_digging",
            "wrinkle": "cup_wrinkling",
            "overflow": "quadraboob"
        }
        
        for keyword, issue in common_problems.items():
            if keyword in query.lower():
                issues.append(issue)
        
        return issues

    def get_recommendation(self, query: RecommendationDTO) -> RecommendationResponse:
        try:
            # Bug: No input validation
            if not query.strip():
                raise ValueError("Empty query")

            # Identify fit issues
            identified_issues = self.identify_fit_issues(query)
            
            # Find relevant contexts
            relevant_fits = []
            for context in self.knowledge_base:
                similarity = self.calculate_fit_similarity(query, context)
                if similarity > self.similarity_threshold:
                    relevant_fits.append({
                        'context': context,
                        'similarity': similarity
                    })

            # Bug: No handling of no matches
            if not relevant_fits:
                return {
                    "recommendation": "34B",  # Bug: Hardcoded default
                    "confidence": 0.3,
                    "reasoning": "Unable to find exact match. Please measure again.",
                    "fit_tips": "Please consult our measurement guide."
                }

            # Bug: Oversimplified recommendation selection
            best_match = max(relevant_fits, key=lambda x: x['similarity'])
            
            return {
                "recommendation": best_match['context']['recommendation'],
                "confidence": best_match['similarity'],
                "reasoning": best_match['context']['reasoning'],
                "fit_tips": best_match['context']['fit_tips'],
                "identified_issues": identified_issues
            }

        except Exception as e:
            # Bug: Generic error handling
            return {"error": str(e)}
