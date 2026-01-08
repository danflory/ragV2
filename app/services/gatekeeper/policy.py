import yaml
import os
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger("Gravitas_POLICY_ENGINE")

class PolicyEngine:
    """
    Evaluates access policies based on Ghost identity and requested resources.
    """
    def __init__(self, policy_path: Optional[str] = None):
        self.policy_path = policy_path or os.getenv("ACCESS_POLICY_PATH", "app/config/access_policies.yaml")
        self.policies = {}
        self.ghost_mappings = {}
        self.load_policies()

    def load_policies(self):
        """Loads policies from YAML file."""
        if not os.path.exists(self.policy_path):
            logger.warning(f"Policy file not found at {self.policy_path}. Using default deny-all.")
            self.policies = {}
            self.ghost_mappings = {}
            return

        try:
            with open(self.policy_path, 'r') as f:
                data = yaml.safe_load(f)
                self.policies = data.get("groups", {})
                self.ghost_mappings = data.get("ghost_mappings", {})
                logger.info(f"Loaded {len(self.policies)} groups and {len(self.ghost_mappings)} ghost mappings.")
        except Exception as e:
            logger.error(f"Failed to load policies: {e}")
            self.policies = {}

    def check_permission(self, ghost_id: str, action: str, resource: str) -> bool:
        """
        Checks if a ghost has permission to perform an action on a resource.
        """
        # 1. Resolve Ghost Groups
        groups = self.ghost_mappings.get(ghost_id, [])
        if not groups and ghost_id == "Supervisor_Managed_Agent":
            # Default fallback for internal agent if not explicitly mapped
            groups = ["admin"]

        if not groups:
            logger.debug(f"Ghost {ghost_id} has no assigned groups.")
            return False

        # 2. Evaluate Permissions across all groups
        for group_name in groups:
            group_policy = self.policies.get(group_name)
            if not group_policy:
                continue

            permissions = group_policy.get("permissions", [])
            for perm in permissions:
                p_action = perm.get("action")
                p_resource = perm.get("resource")

                # Multi-level matching logic
                action_match = (p_action == "*" or p_action == action)
                resource_match = self._resource_match(p_resource, resource)

                if action_match and resource_match:
                    logger.debug(f"Access GRANTED to {ghost_id} for {action} on {resource} via group {group_name}")
                    return True

        logger.info(f"Access DENIED to {ghost_id} for {action} on {resource}")
        return False

    def _resource_match(self, pattern: str, target: str) -> bool:
        """Simple wildcard matching for resources."""
        if pattern == "*":
            return True
        if pattern.endswith("/*"):
            prefix = pattern[:-2]
            return target.startswith(prefix)
        return pattern == target

    def get_effective_permissions(self, ghost_id: str) -> List[Dict]:
        """Returns all combined permissions for a ghost."""
        groups = self.ghost_mappings.get(ghost_id, [])
        effective = []
        for group in groups:
            policy = self.policies.get(group)
            if policy:
                effective.extend(policy.get("permissions", []))
        return effective

# Singleton instance
policy_engine = PolicyEngine()
