"""
Module de génération de rapports
"""

class ReportGenerator:
    """Générateur de rapports"""
    
    def __init__(self, project_path):
        self.project_path = project_path
    
    def generate(self, format='html'):
        """Génère un rapport"""
        if format == 'html':
            return self._generate_html()
        elif format == 'json':
            return self._generate_json()
        elif format == 'text':
            return self._generate_text()
        else:
            return {'error': f'Format {format} non supporté'}
    
    def _generate_html(self):
        """Génère un rapport HTML"""
        return '<html><body>Rapport HTML</body></html>'
    
    def _generate_json(self):
        """Génère un rapport JSON"""
        return {'report': 'json'}
    
    def _generate_text(self):
        """Génère un rapport texte"""
        return 'Rapport texte'
