"""
Human in the Loop - Sistema de interacción humana para mejorar decisiones del agente
Allows human intervention and feedback during agent execution
"""

import json
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


class InterventionType(Enum):
    APPROVAL_REQUEST = "approval_request"
    FEEDBACK_REQUEST = "feedback_request"
    CHOICE_REQUEST = "choice_request"
    REFLECTION_REVIEW = "reflection_review"
    ERROR_RESOLUTION = "error_resolution"


@dataclass
class HumanRequest:
    """Solicitud de intervención humana."""
    request_id: str
    intervention_type: InterventionType
    title: str
    description: str
    context: Dict[str, Any]
    options: List[str] = None
    timeout_seconds: int = 300  # 5 minutos por defecto
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


@dataclass
class HumanResponse:
    """Respuesta del humano a una solicitud."""
    request_id: str
    approved: bool
    selected_option: Optional[str] = None
    feedback: Optional[str] = None
    modifications: Optional[Dict[str, Any]] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class HumanInTheLoop:
    """Sistema principal de Human-in-the-Loop."""
    
    def __init__(self, language: str = "es", auto_approve: bool = False):
        self.language = language
        self.auto_approve = auto_approve
        self.requests_log: List[HumanRequest] = []
        self.responses_log: List[HumanResponse] = []
        self.messages = self._load_messages()
    
    def _load_messages(self) -> Dict:
        """Carga mensajes en el idioma seleccionado."""
        if self.language == "es":
            return {
                "approval_needed": "🤝 Aprobación Humana Requerida",
                "feedback_needed": "💭 Retroalimentación Humana Requerida",
                "choice_needed": "🎯 Selección Humana Requerida",
                "reflection_review": "🔍 Revisión de Reflexión Requerida",
                "error_resolution": "🚨 Resolución de Error Requerida",
                "auto_approved": "✅ Auto-aprobado (modo automático)",
                "waiting_input": "⏳ Esperando entrada del usuario...",
                "timeout_warning": "⚠️ Tiempo límite en",
                "approved": "✅ Aprobado",
                "rejected": "❌ Rechazado",
                "yes": "sí",
                "no": "no", 
                "yes_short": "s",
                "no_short": "n",
                "continue": "continuar",
                "abort": "abortar",
                "retry": "reintentar",
                "modify": "modificar",
                "enter_feedback": "Ingresa tu retroalimentación (opcional):",
                "enter_modifications": "Ingresa modificaciones como JSON (opcional):",
                "invalid_choice": "Opción inválida. Intenta de nuevo.",
                "timeout_reached": "Tiempo límite alcanzado. Procediendo automáticamente...",
                "request_logged": "Solicitud registrada en el historial."
            }
        else:
            return {
                "approval_needed": "🤝 Human Approval Required",
                "feedback_needed": "💭 Human Feedback Required",
                "choice_needed": "🎯 Human Choice Required",
                "reflection_review": "🔍 Reflection Review Required",
                "error_resolution": "🚨 Error Resolution Required",
                "auto_approved": "✅ Auto-approved (automatic mode)",
                "waiting_input": "⏳ Waiting for user input...",
                "timeout_warning": "⚠️ Timeout in",
                "approved": "✅ Approved",
                "rejected": "❌ Rejected",
                "yes": "yes",
                "no": "no",
                "yes_short": "y",
                "no_short": "n",
                "continue": "continue",
                "abort": "abort",
                "retry": "retry",
                "modify": "modify",
                "enter_feedback": "Enter your feedback (optional):",
                "enter_modifications": "Enter modifications as JSON (optional):",
                "invalid_choice": "Invalid choice. Try again.",
                "timeout_reached": "Timeout reached. Proceeding automatically...",
                "request_logged": "Request logged in history."
            }
    
    def request_approval(
        self, 
        title: str, 
        description: str, 
        context: Dict[str, Any] = None,
        timeout_seconds: int = 300
    ) -> HumanResponse:
        """
        Solicita aprobación humana para una acción.
        
        Args:
            title: Título de la solicitud
            description: Descripción detallada
            context: Contexto adicional
            timeout_seconds: Tiempo límite para respuesta
            
        Returns:
            Respuesta humana con aprobación/rechazo
        """
        request_id = f"approval_{int(time.time())}"
        
        request = HumanRequest(
            request_id=request_id,
            intervention_type=InterventionType.APPROVAL_REQUEST,
            title=title,
            description=description,
            context=context or {},
            timeout_seconds=timeout_seconds
        )
        
        return self._handle_request(request)
    
    def request_feedback(
        self, 
        title: str, 
        description: str, 
        context: Dict[str, Any] = None,
        timeout_seconds: int = 300
    ) -> HumanResponse:
        """Solicita retroalimentación humana."""
        request_id = f"feedback_{int(time.time())}"
        
        request = HumanRequest(
            request_id=request_id,
            intervention_type=InterventionType.FEEDBACK_REQUEST,
            title=title,
            description=description,
            context=context or {},
            timeout_seconds=timeout_seconds
        )
        
        return self._handle_request(request)
    
    def request_choice(
        self, 
        title: str, 
        description: str, 
        options: List[str],
        context: Dict[str, Any] = None,
        timeout_seconds: int = 300
    ) -> HumanResponse:
        """Solicita selección entre opciones."""
        request_id = f"choice_{int(time.time())}"
        
        request = HumanRequest(
            request_id=request_id,
            intervention_type=InterventionType.CHOICE_REQUEST,
            title=title,
            description=description,
            context=context or {},
            options=options,
            timeout_seconds=timeout_seconds
        )
        
        return self._handle_request(request)
    
    def request_reflection_review(
        self, 
        reflection_results: List, 
        proposed_action: str,
        context: Dict[str, Any] = None,
        timeout_seconds: int = 300
    ) -> HumanResponse:
        """Solicita revisión de resultados de reflexión."""
        request_id = f"reflection_{int(time.time())}"
        
        description = f"Acción propuesta: {proposed_action}\n\n"
        description += "Resultados de reflexión:\n"
        
        for result in reflection_results:
            status = "✅" if result.passed else "❌"
            description += f"{status} {result.reflection_type.value}: {result.score}/100\n"
            if result.issues:
                description += f"   Problemas: {', '.join(result.issues[:2])}\n"
        
        request = HumanRequest(
            request_id=request_id,
            intervention_type=InterventionType.REFLECTION_REVIEW,
            title="Revisión de Calidad de Código",
            description=description,
            context={
                "reflection_results": [asdict(r) for r in reflection_results],
                "proposed_action": proposed_action,
                **(context or {})
            },
            options=["continuar", "modificar", "abortar"],
            timeout_seconds=timeout_seconds
        )
        
        return self._handle_request(request)
    
    def request_error_resolution(
        self, 
        error: str, 
        attempted_action: str,
        context: Dict[str, Any] = None,
        timeout_seconds: int = 300
    ) -> HumanResponse:
        """Solicita ayuda para resolver un error."""
        request_id = f"error_{int(time.time())}"
        
        description = f"Error encontrado: {error}\n"
        description += f"Acción intentada: {attempted_action}\n\n"
        description += "¿Cómo proceder?"
        
        request = HumanRequest(
            request_id=request_id,
            intervention_type=InterventionType.ERROR_RESOLUTION,
            title="Resolución de Error",
            description=description,
            context={
                "error": error,
                "attempted_action": attempted_action,
                **(context or {})
            },
            options=["reintentar", "modificar", "abortar"],
            timeout_seconds=timeout_seconds
        )
        
        return self._handle_request(request)
    
    def _handle_request(self, request: HumanRequest) -> HumanResponse:
        """Maneja una solicitud de intervención humana."""
        self.requests_log.append(request)
        
        # Modo automático
        if self.auto_approve:
            print(f"🤖 {self.messages['auto_approved']}")
            response = HumanResponse(
                request_id=request.request_id,
                approved=True,
                selected_option=request.options[0] if request.options else None,
                feedback="Auto-aprobado en modo automático"
            )
            self.responses_log.append(response)
            return response
        
        # Mostrar solicitud
        self._display_request(request)
        
        # Obtener respuesta del usuario
        response = self._get_user_response(request)
        
        self.responses_log.append(response)
        print(f"📝 {self.messages['request_logged']}")
        
        return response
    
    def _display_request(self, request: HumanRequest):
        """Muestra la solicitud al usuario."""
        print("\n" + "="*60)
        
        if request.intervention_type == InterventionType.APPROVAL_REQUEST:
            print(f"🤝 {self.messages['approval_needed']}")
        elif request.intervention_type == InterventionType.FEEDBACK_REQUEST:
            print(f"💭 {self.messages['feedback_needed']}")
        elif request.intervention_type == InterventionType.CHOICE_REQUEST:
            print(f"🎯 {self.messages['choice_needed']}")
        elif request.intervention_type == InterventionType.REFLECTION_REVIEW:
            print(f"🔍 {self.messages['reflection_review']}")
        elif request.intervention_type == InterventionType.ERROR_RESOLUTION:
            print(f"🚨 {self.messages['error_resolution']}")
        
        print(f"\n📌 {request.title}")
        print(f"📝 {request.description}")
        
        if request.context:
            print(f"\n📊 Contexto:")
            for key, value in request.context.items():
                if isinstance(value, (str, int, float, bool)):
                    print(f"   {key}: {value}")
        
        if request.options:
            print(f"\n📋 Opciones:")
            for i, option in enumerate(request.options, 1):
                print(f"   {i}. {option}")
        
        print("="*60)
    
    def _get_user_response(self, request: HumanRequest) -> HumanResponse:
        """Obtiene la respuesta del usuario."""
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            remaining = request.timeout_seconds - elapsed
            
            if remaining <= 0:
                print(f"\n⏰ {self.messages['timeout_reached']}")
                return HumanResponse(
                    request_id=request.request_id,
                    approved=True,  # Aprobar por defecto en timeout
                    feedback="Timeout - aprobado automáticamente"
                )
            
            if remaining <= 60:
                print(f"\n⚠️ {self.messages['timeout_warning']} {remaining:.0f}s")
            
            try:
                if request.intervention_type == InterventionType.APPROVAL_REQUEST:
                    return self._get_approval_response(request)
                elif request.intervention_type == InterventionType.FEEDBACK_REQUEST:
                    return self._get_feedback_response(request)
                elif request.intervention_type == InterventionType.CHOICE_REQUEST:
                    return self._get_choice_response(request)
                elif request.intervention_type == InterventionType.REFLECTION_REVIEW:
                    return self._get_choice_response(request)
                elif request.intervention_type == InterventionType.ERROR_RESOLUTION:
                    return self._get_choice_response(request)
                    
            except KeyboardInterrupt:
                print(f"\n❌ Operación cancelada por el usuario")
                return HumanResponse(
                    request_id=request.request_id,
                    approved=False,
                    feedback="Cancelado por el usuario"
                )
    
    def _get_approval_response(self, request: HumanRequest) -> HumanResponse:
        """Obtiene respuesta de aprobación."""
        prompt = f"\n🤝 ¿Aprobar esta acción? ({self.messages['yes_short']}/{self.messages['no_short']}): "
        user_input = input(prompt).strip().lower()
        
        if user_input in [self.messages['yes'], self.messages['yes_short'], '1']:
            approved = True
            status_msg = self.messages['approved']
        elif user_input in [self.messages['no'], self.messages['no_short'], '0']:
            approved = False
            status_msg = self.messages['rejected']
        else:
            print(f"❌ {self.messages['invalid_choice']}")
            return self._get_approval_response(request)
        
        # Solicitar feedback opcional
        feedback_prompt = f"\n💭 {self.messages['enter_feedback']} "
        feedback = input(feedback_prompt).strip()
        
        print(f"\n{status_msg}")
        
        return HumanResponse(
            request_id=request.request_id,
            approved=approved,
            feedback=feedback if feedback else None
        )
    
    def _get_feedback_response(self, request: HumanRequest) -> HumanResponse:
        """Obtiene respuesta de retroalimentación."""
        prompt = f"\n💭 {self.messages['enter_feedback']} "
        feedback = input(prompt).strip()
        
        modifications_prompt = f"\n🔧 {self.messages['enter_modifications']} "
        modifications_str = input(modifications_prompt).strip()
        
        modifications = None
        if modifications_str:
            try:
                modifications = json.loads(modifications_str)
            except json.JSONDecodeError:
                print("❌ JSON inválido para modificaciones")
        
        return HumanResponse(
            request_id=request.request_id,
            approved=True,  # Feedback siempre aprobado
            feedback=feedback if feedback else None,
            modifications=modifications
        )
    
    def _get_choice_response(self, request: HumanRequest) -> HumanResponse:
        """Obtiene respuesta de selección."""
        prompt = f"\n🎯 Selecciona una opción (1-{len(request.options)}): "
        
        try:
            choice_num = int(input(prompt).strip())
            if 1 <= choice_num <= len(request.options):
                selected_option = request.options[choice_num - 1]
                print(f"\n✅ Seleccionado: {selected_option}")
                
                return HumanResponse(
                    request_id=request.request_id,
                    approved=True,
                    selected_option=selected_option
                )
            else:
                print(f"❌ {self.messages['invalid_choice']}")
                return self._get_choice_response(request)
                
        except ValueError:
            print(f"❌ {self.messages['invalid_choice']}")
            return self._get_choice_response(request)
    
    def get_history(self) -> Dict[str, List]:
        """Obtiene el historial de solicitudes y respuestas."""
        return {
            "requests": [asdict(req) for req in self.requests_log],
            "responses": [asdict(resp) for resp in self.responses_log]
        }
    
    def save_history(self, file_path: str):
        """Guarda el historial en un archivo."""
        history = self.get_history()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def load_history(self, file_path: str):
        """Carga el historial desde un archivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            self.requests_log = [
                HumanRequest(**req) for req in history.get("requests", [])
            ]
            self.responses_log = [
                HumanResponse(**resp) for resp in history.get("responses", [])
            ]
        except Exception as e:
            print(f"Error cargando historial: {e}")
    
    def clear_history(self):
        """Limpia el historial."""
        self.requests_log.clear()
        self.responses_log.clear()
    
    def set_auto_approve(self, auto_approve: bool):
        """Activa/desactiva el modo de aprobación automática."""
        self.auto_approve = auto_approve
        mode = "automático" if auto_approve else "manual"
        print(f"🔧 Modo cambiado a: {mode}")


# Funciones de utilidad
def create_human_loop(language: str = "es", auto_approve: bool = False) -> HumanInTheLoop:
    """Crea una instancia del sistema Human-in-the-Loop."""
    return HumanInTheLoop(language=language, auto_approve=auto_approve)


def quick_approval(title: str, description: str, human_loop: HumanInTheLoop = None) -> bool:
    """Función rápida para solicitar aprobación."""
    if human_loop is None:
        human_loop = create_human_loop()
    
    response = human_loop.request_approval(title, description)
    return response.approved
