from typing import Dict, Any, List
import re
from datetime import datetime
import yaml
from ..schemas.schemas import Rule, RuleMatch, SecurityEvent
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class RuleEngine:
    def __init__(self):
        self.rules: Dict[str, Rule] = {}
        self.compiled_rules: Dict[str, Any] = {}
        
    async def load_rules(self, rules_path: str) -> None:
        """Load rules from YAML configuration"""
        try:
            with open(rules_path, 'r') as f:
                rule_configs = yaml.safe_load(f)
                
            for rule_config in rule_configs:
                rule = Rule(
                    id=rule_config["id"],
                    name=rule_config["name"],
                    description=rule_config.get("description", ""),
                    severity=rule_config["severity"],
                    conditions=rule_config["conditions"],
                    actions=rule_config["actions"]
                )
                await self.add_rule(rule)
                
        except Exception as e:
            logger.error(f"Error loading rules: {str(e)}")
            raise
            
    async def add_rule(self, rule: Rule) -> None:
        """Add a new detection rule"""
        try:
            # Validate rule syntax
            self._validate_rule(rule)
            
            # Compile rule conditions
            compiled_rule = self._compile_rule(rule)
            
            # Store rule
            self.rules[rule.id] = rule
            self.compiled_rules[rule.id] = compiled_rule
            
            logger.info(f"Added rule: {rule.id} - {rule.name}")
            
        except Exception as e:
            logger.error(f"Error adding rule {rule.id}: {str(e)}")
            raise
            
    async def evaluate_event(self, event: SecurityEvent) -> List[RuleMatch]:
        """Evaluate an event against all rules"""
        matches = []
        
        try:
            event_dict = self._event_to_dict(event)
            
            for rule_id, compiled_rule in self.compiled_rules.items():
                if self._matches_rule(event_dict, compiled_rule):
                    rule = self.rules[rule_id]
                    match = RuleMatch(
                        rule_id=rule_id,
                        event_id=event.id,
                        timestamp=datetime.utcnow(),
                        severity=rule.severity,
                        matched_conditions=self._get_matched_conditions(
                            event_dict,
                            compiled_rule
                        )
                    )
                    matches.append(match)
                    
                    # Execute rule actions
                    await self._execute_actions(rule, event)
                    
            return matches
            
        except Exception as e:
            logger.error(f"Error evaluating rules: {str(e)}")
            raise
            
    def _validate_rule(self, rule: Rule) -> None:
        """Validate rule syntax and structure"""
        required_fields = ["id", "name", "severity", "conditions"]
        for field in required_fields:
            if not getattr(rule, field):
                raise ValueError(f"Missing required field: {field}")
                
        # Validate conditions syntax
        for condition in rule.conditions:
            if "field" not in condition or "operator" not in condition:
                raise ValueError(f"Invalid condition in rule {rule.id}")
                
        # Validate severity level
        valid_severities = ["low", "medium", "high", "critical"]
        if rule.severity not in valid_severities:
            raise ValueError(f"Invalid severity level in rule {rule.id}")
            
    def _compile_rule(self, rule: Rule) -> Dict[str, Any]:
        """Compile rule conditions for efficient matching"""
        compiled = {
            "conditions": [],
            "logic": rule.logic or "AND"
        }
        
        for condition in rule.conditions:
            compiled_condition = {
                "field": condition["field"],
                "operator": condition["operator"],
                "value": condition["value"]
            }
            
            # Precompile regex patterns
            if condition["operator"] == "matches":
                compiled_condition["pattern"] = re.compile(condition["value"])
                
            compiled["conditions"].append(compiled_condition)
            
        return compiled
        
    def _matches_rule(self, event: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        """Check if event matches rule conditions"""
        results = []
        
        for condition in rule["conditions"]:
            field_value = self._get_field_value(event, condition["field"])
            result = self._evaluate_condition(field_value, condition)
            results.append(result)
            
        # Combine results based on logic
        if rule["logic"] == "AND":
            return all(results)
        elif rule["logic"] == "OR":
            return any(results)
        else:
            raise ValueError(f"Invalid rule logic: {rule['logic']}")
            
    def _evaluate_condition(
        self,
        field_value: Any,
        condition: Dict[str, Any]
    ) -> bool:
        """Evaluate a single condition"""
        operator = condition["operator"]
        expected_value = condition["value"]
        
        if operator == "equals":
            return field_value == expected_value
        elif operator == "not_equals":
            return field_value != expected_value
        elif operator == "greater_than":
            return field_value > expected_value
        elif operator == "less_than":
            return field_value < expected_value
        elif operator == "contains":
            return expected_value in field_value
        elif operator == "matches":
            return bool(condition["pattern"].match(str(field_value)))
        else:
            raise ValueError(f"Invalid operator: {operator}")
            
    async def _execute_actions(self, rule: Rule, event: SecurityEvent) -> None:
        """Execute actions for matched rule"""
        for action in rule.actions:
            try:
                if action["type"] == "alert":
                    await self._send_alert(rule, event, action)
                elif action["type"] == "block":
                    await self._block_threat(event, action)
                elif action["type"] == "isolate":
                    await self._isolate_system(event, action)
                else:
                    logger.warning(f"Unknown action type: {action['type']}")
                    
            except Exception as e:
                logger.error(f"Error executing action: {str(e)}") 