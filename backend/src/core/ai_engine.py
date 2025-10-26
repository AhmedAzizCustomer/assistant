"""Core AI engine for the personal assistant."""
from typing import Optional, Dict, Any, List
from anthropic import Anthropic
from openai import OpenAI
from .config import get_settings


class AIEngine:
    """Main AI engine that orchestrates Claude and OpenAI."""

    def __init__(self):
        """Initialize AI engine with both providers."""
        settings = get_settings()

        # Store settings but don't create clients yet (lazy initialization)
        self.anthropic_api_key = settings.anthropic_api_key
        self.openai_api_key = settings.openai_api_key
        self.default_provider = settings.default_ai_provider
        self.claude_model = settings.claude_model
        self.openai_model = settings.openai_model

        # Clients are created lazily when needed
        self._anthropic_client = None
        self._openai_client = None

    @property
    def anthropic_client(self):
        """Get or create Anthropic client."""
        if self._anthropic_client is None and self.anthropic_api_key:
            self._anthropic_client = Anthropic(api_key=self.anthropic_api_key)
        return self._anthropic_client

    @property
    def openai_client(self):
        """Get or create OpenAI client."""
        if self._openai_client is None and self.openai_api_key:
            self._openai_client = OpenAI(api_key=self.openai_api_key)
        return self._openai_client

    async def generate_response(
        self,
        prompt: str,
        context: Optional[str] = None,
        provider: Optional[str] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
    ) -> str:
        """
        Generate a response using the specified AI provider.

        Args:
            prompt: The user's prompt
            context: Additional context for the AI
            provider: 'anthropic' or 'openai', defaults to configured default
            system_prompt: System instructions for the AI
            max_tokens: Maximum tokens in response

        Returns:
            The AI's response as a string
        """
        provider = provider or self.default_provider

        # Check if API keys are configured
        if provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("Anthropic API key not configured. Please configure it in Settings.")
        if provider == "openai" and not self.openai_api_key:
            raise ValueError("OpenAI API key not configured. Please configure it in Settings.")

        # Combine context and prompt
        full_prompt = f"{context}\n\n{prompt}" if context else prompt

        if provider == "anthropic":
            return await self._generate_claude(full_prompt, system_prompt, max_tokens)
        elif provider == "openai":
            return await self._generate_openai(full_prompt, system_prompt, max_tokens)
        else:
            raise ValueError(f"Unknown AI provider: {provider}")

    async def _generate_claude(
        self, prompt: str, system_prompt: Optional[str], max_tokens: int
    ) -> str:
        """Generate response using Claude."""
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")

        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": self.claude_model,
            "max_tokens": max_tokens,
            "messages": messages,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.anthropic_client.messages.create(**kwargs)
        return response.content[0].text

    async def _generate_openai(
        self, prompt: str, system_prompt: Optional[str], max_tokens: int
    ) -> str:
        """Generate response using OpenAI."""
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.openai_client.chat.completions.create(
            model=self.openai_model, messages=messages, max_tokens=max_tokens
        )

        return response.choices[0].message.content

    async def analyze_email(self, email_content: str, email_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an email and provide insights.

        Args:
            email_content: The email body
            email_metadata: Email metadata (from, subject, date, etc.)

        Returns:
            Analysis including priority, category, summary, and suggested actions
        """
        system_prompt = """You are an email analysis assistant. Analyze emails and provide:
        1. Priority level (high, medium, low)
        2. Category (work, personal, promotional, social, etc.)
        3. Brief summary
        4. Suggested actions (reply, schedule, delegate, archive, etc.)
        5. Sentiment (positive, neutral, negative)

        Return your analysis in a structured format."""

        prompt = f"""
        From: {email_metadata.get('from', 'Unknown')}
        Subject: {email_metadata.get('subject', 'No subject')}
        Date: {email_metadata.get('date', 'Unknown')}

        Email Content:
        {email_content}

        Please analyze this email and provide your assessment in JSON format.
        """

        response = await self.generate_response(prompt, system_prompt=system_prompt)

        # Parse response (simplified - you may want more robust parsing)
        return {
            "raw_analysis": response,
            "email_id": email_metadata.get("id"),
        }

    async def draft_email_response(
        self, original_email: str, context: str, tone: str = "professional"
    ) -> str:
        """
        Draft a response to an email.

        Args:
            original_email: The original email content
            context: Additional context or instructions
            tone: Desired tone (professional, casual, formal, friendly)

        Returns:
            Drafted email response
        """
        system_prompt = f"""You are an email writing assistant. Draft email responses that are:
        - {tone} in tone
        - Clear and concise
        - Appropriate to the context
        - Well-structured

        Only provide the email body, no subject line."""

        prompt = f"""
        Original Email:
        {original_email}

        Instructions: {context}

        Please draft an appropriate response.
        """

        return await self.generate_response(prompt, system_prompt=system_prompt)

    async def optimize_schedule(
        self, tasks: List[Dict[str, Any]], constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Optimize a schedule based on tasks and constraints.

        Args:
            tasks: List of tasks with priorities, durations, deadlines
            constraints: Scheduling constraints (work hours, breaks, preferences)

        Returns:
            Optimized schedule with time blocks
        """
        system_prompt = """You are a schedule optimization assistant. Create optimal schedules that:
        - Respect time constraints and deadlines
        - Balance work and rest
        - Prioritize important tasks
        - Include buffer time
        - Consider energy levels and productivity patterns"""

        prompt = f"""
        Tasks to schedule:
        {tasks}

        Constraints:
        {constraints}

        Please create an optimized schedule in JSON format with time blocks.
        """

        response = await self.generate_response(prompt, system_prompt=system_prompt)
        return {"schedule": response, "tasks_count": len(tasks)}

    async def generate_meal_plan(
        self, preferences: Dict[str, Any], days: int = 7
    ) -> Dict[str, Any]:
        """
        Generate a meal plan based on dietary preferences.

        Args:
            preferences: Dietary preferences, restrictions, goals, calories
            days: Number of days to plan for

        Returns:
            Meal plan with recipes and nutrition info
        """
        system_prompt = """You are a nutrition and meal planning expert. Create meal plans that:
        - Meet nutritional requirements
        - Respect dietary restrictions
        - Are practical and achievable
        - Include variety
        - Provide calorie and macro information
        - Include grocery lists"""

        prompt = f"""
        Create a {days}-day meal plan with these preferences:
        {preferences}

        Include breakfast, lunch, dinner, and snacks.
        Provide recipes and nutritional information in JSON format.
        """

        response = await self.generate_response(
            prompt, system_prompt=system_prompt, max_tokens=8000
        )
        return {"meal_plan": response, "days": days}

    async def create_workout_plan(
        self, fitness_level: str, goals: str, constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a personalized workout plan.

        Args:
            fitness_level: beginner, intermediate, advanced
            goals: Fitness goals (weight loss, muscle gain, endurance, etc.)
            constraints: Time available, equipment, injuries, etc.

        Returns:
            Workout plan with exercises and schedule
        """
        system_prompt = """You are a fitness and exercise planning expert. Create workout plans that:
        - Match the user's fitness level
        - Align with their goals
        - Respect constraints and limitations
        - Include proper warm-up and cool-down
        - Provide progressive overload
        - Are safe and effective"""

        prompt = f"""
        Create a workout plan for:
        - Fitness Level: {fitness_level}
        - Goals: {goals}
        - Constraints: {constraints}

        Provide a detailed plan in JSON format with exercises, sets, reps, and schedule.
        """

        response = await self.generate_response(
            prompt, system_prompt=system_prompt, max_tokens=6000
        )
        return {"workout_plan": response}

    async def chat(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        user_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Chat interface for conversational AI assistant.

        Args:
            message: User's message
            conversation_history: Previous conversation messages
            user_context: User's current context (calendar, tasks, etc.)

        Returns:
            Assistant's response
        """
        system_prompt = """You are a helpful AI personal assistant. You help users with:
        - Email management
        - Calendar and scheduling
        - Task management
        - Meal planning and diet tracking
        - Exercise planning and tracking
        - Event management
        - General productivity

        Be conversational, helpful, and proactive. Provide actionable suggestions."""

        # Build context from conversation history
        context = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in conversation_history[-5:]  # Last 5 messages
        ])

        if user_context:
            context += f"\n\nUser Context: {user_context}"

        return await self.generate_response(
            message, context=context, system_prompt=system_prompt
        )
