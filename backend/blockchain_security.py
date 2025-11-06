import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import threading

class Block:
    def __init__(self, index: int, data: Dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class AETHERBlockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 1
        self.lock = threading.Lock()
    
    def create_genesis_block(self) -> Block:
        return Block(0, {"message": "AETHER Genesis Block"}, "0")
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def add_vehicle_data(self, vehicle_id: str, data: Dict[str, Any]) -> bool:
        try:
            with self.lock:
                block_data = {
                    "type": "VEHICLE_DATA",
                    "vehicle_id": vehicle_id,
                    "timestamp": datetime.now().isoformat(),
                    "data": data,
                    "hash_verification": hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
                }
                
                new_block = Block(
                    len(self.chain),
                    block_data,
                    self.get_latest_block().hash
                )
                new_block.mine_block(self.difficulty)
                self.chain.append(new_block)
                return True
        except Exception as e:
            print(f"Blockchain error: {e}")
            return False
    
    def verify_data_integrity(self, vehicle_id: str) -> Dict[str, Any]:
        vehicle_blocks = [block for block in self.chain if 
                         block.data.get("vehicle_id") == vehicle_id]
        
        return {
            "total_records": len(vehicle_blocks),
            "chain_valid": self.is_chain_valid(),
            "last_update": vehicle_blocks[-1].timestamp if vehicle_blocks else None,
            "integrity_score": 100.0 if self.is_chain_valid() else 0.0
        }
    
    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_vehicle_history(self, vehicle_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "timestamp": block.timestamp,
                "data": block.data,
                "hash": block.hash,
                "verified": True
            }
            for block in self.chain 
            if block.data.get("vehicle_id") == vehicle_id
        ]

# Global blockchain instance
aether_blockchain = AETHERBlockchain()