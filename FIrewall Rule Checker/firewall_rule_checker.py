from typing import List, Dict, Optional
from ipaddress import IPv4Address, IPv4Network
from dataclasses import dataclass
from enum import Enum


class Action(Enum):
    ALLOW = "allow"
    DENY = "deny"

class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ANY = "any"

@dataclass
class FirewallRule:
    id: str
    source_ip: str
    destination_ip: str
    protocol: Protocol
    source_port: Optional[int]
    destination_port: Optional[int]
    action: Action


class FirewallRuleChecker:
    def __init__(self) -> None:
        self.rules: List[FirewallRule] = []

    def add_rule(self, rule: FirewallRule) -> None:
        """Add a new firewall rule to the checker"""
        self.rules.append(rule)

    def validate_rule(self,rule: FirewallRule) -> List[str]:
        """Validate a  firewall rule for common protocols"""
        issues=[]

        #check ip addresses
        try:
            IPv4Address(rule.source_ip) if '/' not in rule.source_ip else IPv4Network(rule.source_ip)
        except ValueError:
            issues.append(f"Invalid source IP address: {rule.source_ip}")

        try:
            IPv4Address(rule.destination_ip) if '/' not in rule.destination_ip else IPv4Network(rule.destination_ip)
        except ValueError:
            issues.append(f"Invalid destination IP address: {rule.destination_ip}")

        #validate ports
        if rule.protocol in [Protocol.TCP,Protocol.UDP]:
            if rule.source_port is not None and not (0 <= rule.source_port <= 65535):
                issues.append(f"Invalid source port : {rule.source_port}")
        if rule.destination_port is not None and not (0 <= rule.destination_port <= 65535):
            issues.append(f"Invalid destination port : {rule.destination_port}")
        
        return issues

    def find_conflicting_rules(self)-> List[tuple[FirewallRule, FirewallRule]]:
        """Find conflicting rules"""
        conflicts = []
        for i, rule1 in enumerate(self.rules):
            for rule2 in self.rules[i+1:]:
                if self._rules_conflict(rule1,rule2):
                    conflicts.append((rule1,rule2))
        return conflicts

    def _rules_conflict(self,rule1:FirewallRule,rule2:FirewallRule)-> bool:
        """Check if two rules conflict"""
        if rule1.action != rule2.action:
            #check if ip ranges overlap
            if self._ip_ranges_overlap(rule1.source_ip,rule2.source_ip) and self._ip_ranges_overlap(rule1.destination_ip,rule2.destination_ip):
                #check if protocals match or if either is ANY
                if rule1.protocol == rule2.protocol or rule1.protocol == Protocol.ANY or rule2.protocol == Protocol.ANY:
                    #check if ports overlap
                    if self._ports_overlap(rule1.source_port,rule2.source_port) and self._ports_overlap(rule1.destination_port,rule2.destination_port):
                        return True
        return False

    def _ip_ranges_overlap(self,ip1: str, ip2: str) -> bool:
        """Check if two ip ranges overlap"""
        try:
            net1 = IPv4Network(ip1) if '/' in ip1 else IPv4Address(f"{ip1}/32")
            net2 = IPv4Network(ip2) if '/' in ip2 else IPv4Address(f"{ip2}/32")
            return net1.overlaps(net2)
        except ValueError:
            return False

    def _ports_overlap(self, port1: int, port2: int) -> bool:
        """Check if two ports overlap"""
        return port1 == port2 or (port1 is not None and port2 is not None and (port1 <= port2 <= port1 or port2 <= port1 <= port2))

    def check_coverage(self,target_network:str)->Dict[str,bool]:
        """Check if the firewall rules cover the target network"""
        coverage = {
            "allowed":False,
            "denied":False
        }
        target = IPv4Network(target_network)
        for rule in self.rules:
            if self._ip_ranges_overlap(target_network,rule.destination_ip):
                if rule.action == Action.ALLOW:
                    coverage["allowed"] = True
                else:
                    coverage["denied"] = True
        return coverage


#Example usage
def main():
    checker = FirewallRuleChecker()

    # add some example rules

    rules =[
        FirewallRule(
            id="rule1",
            source_ip="192.168.1.0/24",
            destination_ip="10.0.0.0/8",
            protocol=Protocol.TCP,
            source_port=None,
            destination_port=80,
            action=Action.ALLOW
        ),
        FirewallRule(
            id="rule2",
            source_ip="192.168.1.100",
            destination_ip="10.0.0.5",
            protocol=Protocol.TCP,
            source_port=None,
            destination_port=80,
            action=Action.DENY
        )
    ]

    for rule in rules:
        #validate rule before adding
        issues = checker.validate_rule(rule)
        if issues:
            print(f"Issues found in rule {rule.id}: ")
            for issue in issues:
                print(f"- {issue}")
        else:
            checker.add_rule(rule)
            print(f"Added rule {rule.id}")

    #check for conflicts
    conflicts = checker.find_conflicting_rules()
    if conflicts:
        print("\nConflicting rules found: ")
        for rule1,rule2 in conflicts:
            print(f"Conflict between rules {rule1.id} and {rule2.id}")
    
    #check coverage for a specific network
    target = "10.0.0.0/24"
    coverage = checker.check_coverage(target)
    print(f"\nCoverage for {target}: ")
    print(f"Allowed: {coverage['allowed']}")
    print(f"Denied: {coverage['denied']}")

if __name__ == "__main__":
    main()
