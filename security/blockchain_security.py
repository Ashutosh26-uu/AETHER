import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class Block:
    def __init__(self, index: int, transactions: List[Dict], timestamp: float, previous_hash: str):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate the hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """Mine the block with proof of work"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class AETHERBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 10
        self.encryption_key = self._generate_encryption_key()
    
    def create_genesis_block(self) -> Block:
        """Create the first block in the blockchain"""
        return Block(0, [], time.time(), "0")
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key for sensitive data"""
        password = b"aether_security_key_2024"
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def get_latest_block(self) -> Block:
        """Get the latest block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Dict[str, Any]):
        """Add a new transaction to pending transactions"""
        # Encrypt sensitive data
        encrypted_transaction = self._encrypt_transaction_data(transaction)
        self.pending_transactions.append(encrypted_transaction)
    
    def _encrypt_transaction_data(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive transaction data"""
        fernet = Fernet(self.encryption_key)
        
        # Encrypt sensitive fields
        sensitive_fields = ['vehicle_data', 'location', 'personal_info']
        encrypted_transaction = transaction.copy()
        
        for field in sensitive_fields:
            if field in transaction:
                data_bytes = json.dumps(transaction[field]).encode()
                encrypted_data = fernet.encrypt(data_bytes)
                encrypted_transaction[field] = base64.b64encode(encrypted_data).decode()
                encrypted_transaction[f'{field}_encrypted'] = True
        
        return encrypted_transaction
    
    def _decrypt_transaction_data(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt sensitive transaction data"""
        fernet = Fernet(self.encryption_key)
        
        decrypted_transaction = transaction.copy()
        
        for key, value in transaction.items():
            if key.endswith('_encrypted') and value:
                field_name = key.replace('_encrypted', '')
                if field_name in transaction:
                    try:
                        encrypted_data = base64.b64decode(transaction[field_name].encode())
                        decrypted_data = fernet.decrypt(encrypted_data)
                        decrypted_transaction[field_name] = json.loads(decrypted_data.decode())
                    except Exception as e:
                        print(f"Error decrypting {field_name}: {e}")
        
        return decrypted_transaction
    
    def mine_pending_transactions(self, mining_reward_address: str):
        """Mine all pending transactions"""
        reward_transaction = {
            'from': None,
            'to': mining_reward_address,
            'amount': self.mining_reward,
            'type': 'mining_reward',
            'timestamp': datetime.now().isoformat()
        }
        
        self.pending_transactions.append(reward_transaction)
        
        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.get_latest_block().hash
        )
        
        block.mine_block(self.difficulty)
        
        print(f"Block successfully mined with {len(self.pending_transactions)} transactions")
        self.chain.append(block)
        self.pending_transactions = []
    
    def create_vehicle_data_transaction(self, vehicle_id: str, data: Dict[str, Any]) -> str:
        """Create a transaction for vehicle data"""
        transaction = {
            'transaction_id': self._generate_transaction_id(),
            'type': 'vehicle_data',
            'vehicle_id': vehicle_id,
            'vehicle_data': data,
            'timestamp': datetime.now().isoformat(),
            'data_hash': self._calculate_data_hash(data)
        }
        
        self.add_transaction(transaction)
        return transaction['transaction_id']
    
    def create_emergency_transaction(self, vehicle_id: str, emergency_data: Dict[str, Any]) -> str:
        """Create a transaction for emergency events"""
        transaction = {
            'transaction_id': self._generate_transaction_id(),
            'type': 'emergency_alert',
            'vehicle_id': vehicle_id,
            'emergency_data': emergency_data,
            'priority': 'CRITICAL',
            'timestamp': datetime.now().isoformat(),
            'data_hash': self._calculate_data_hash(emergency_data)
        }
        
        self.add_transaction(transaction)
        return transaction['transaction_id']
    
    def create_maintenance_transaction(self, vehicle_id: str, maintenance_data: Dict[str, Any]) -> str:
        """Create a transaction for maintenance records"""
        transaction = {
            'transaction_id': self._generate_transaction_id(),
            'type': 'maintenance_record',
            'vehicle_id': vehicle_id,
            'maintenance_data': maintenance_data,
            'timestamp': datetime.now().isoformat(),
            'data_hash': self._calculate_data_hash(maintenance_data)
        }
        
        self.add_transaction(transaction)
        return transaction['transaction_id']
    
    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID"""
        return hashlib.sha256(f"{time.time()}{os.urandom(16)}".encode()).hexdigest()[:16]
    
    def _calculate_data_hash(self, data: Dict[str, Any]) -> str:
        """Calculate hash of data for integrity verification"""
        data_string = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def verify_data_integrity(self, transaction_id: str, data: Dict[str, Any]) -> bool:
        """Verify data integrity using blockchain"""
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('transaction_id') == transaction_id:
                    stored_hash = transaction.get('data_hash')
                    current_hash = self._calculate_data_hash(data)
                    return stored_hash == current_hash
        return False
    
    def get_vehicle_history(self, vehicle_id: str) -> List[Dict[str, Any]]:
        """Get complete history of a vehicle from blockchain"""
        vehicle_transactions = []
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('vehicle_id') == vehicle_id:
                    # Decrypt transaction data
                    decrypted_transaction = self._decrypt_transaction_data(transaction)
                    decrypted_transaction['block_index'] = block.index
                    decrypted_transaction['block_hash'] = block.hash
                    vehicle_transactions.append(decrypted_transaction)
        
        return sorted(vehicle_transactions, key=lambda x: x.get('timestamp', ''))
    
    def validate_chain(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {i}")
                return False
        
        return True
    
    def get_blockchain_stats(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        total_transactions = sum(len(block.transactions) for block in self.chain)
        
        transaction_types = {}
        for block in self.chain:
            for transaction in block.transactions:
                tx_type = transaction.get('type', 'unknown')
                transaction_types[tx_type] = transaction_types.get(tx_type, 0) + 1
        
        return {
            'total_blocks': len(self.chain),
            'total_transactions': total_transactions,
            'pending_transactions': len(self.pending_transactions),
            'transaction_types': transaction_types,
            'chain_valid': self.validate_chain(),
            'latest_block_hash': self.get_latest_block().hash,
            'difficulty': self.difficulty
        }

class SecurityManager:
    def __init__(self):
        self.blockchain = AETHERBlockchain()
        self.access_tokens = {}
        self.failed_attempts = {}
        self.max_failed_attempts = 5
    
    def generate_access_token(self, user_id: str, permissions: List[str]) -> str:
        """Generate JWT-like access token"""
        token_data = {
            'user_id': user_id,
            'permissions': permissions,
            'issued_at': datetime.now().isoformat(),
            'expires_at': (datetime.now().timestamp() + 3600)  # 1 hour
        }
        
        token = base64.b64encode(json.dumps(token_data).encode()).decode()
        self.access_tokens[token] = token_data
        return token
    
    def validate_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate access token"""
        if token not in self.access_tokens:
            return None
        
        token_data = self.access_tokens[token]
        if datetime.now().timestamp() > token_data['expires_at']:
            del self.access_tokens[token]
            return None
        
        return token_data
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events to blockchain"""
        security_transaction = {
            'transaction_id': self.blockchain._generate_transaction_id(),
            'type': 'security_event',
            'event_type': event_type,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
        self.blockchain.add_transaction(security_transaction)
    
    def check_rate_limiting(self, user_id: str) -> bool:
        """Check if user has exceeded rate limits"""
        if user_id in self.failed_attempts:
            if self.failed_attempts[user_id] >= self.max_failed_attempts:
                return False
        return True
    
    def record_failed_attempt(self, user_id: str):
        """Record failed authentication attempt"""
        self.failed_attempts[user_id] = self.failed_attempts.get(user_id, 0) + 1
        
        self.log_security_event('failed_authentication', {
            'user_id': user_id,
            'attempt_count': self.failed_attempts[user_id],
            'ip_address': 'unknown'  # Would be populated in real implementation
        })

# Example usage
if __name__ == "__main__":
    # Initialize security system
    security_manager = SecurityManager()
    blockchain = security_manager.blockchain
    
    # Create sample vehicle data transaction
    vehicle_data = {
        'speed': 65,
        'location': {'lat': 28.6139, 'lon': 77.2090},
        'health_score': 85,
        'fuel_level': 70
    }
    
    tx_id = blockchain.create_vehicle_data_transaction('AETHER_001', vehicle_data)
    print(f"Vehicle data transaction created: {tx_id}")
    
    # Create emergency transaction
    emergency_data = {
        'type': 'collision_detected',
        'severity': 'high',
        'location': {'lat': 28.6140, 'lon': 77.2091},
        'emergency_services_notified': True
    }
    
    emergency_tx_id = blockchain.create_emergency_transaction('AETHER_001', emergency_data)
    print(f"Emergency transaction created: {emergency_tx_id}")
    
    # Mine pending transactions
    blockchain.mine_pending_transactions('miner_address_001')
    
    # Get blockchain stats
    stats = blockchain.get_blockchain_stats()
    print(f"Blockchain Stats: {json.dumps(stats, indent=2)}")
    
    # Verify data integrity
    is_valid = blockchain.verify_data_integrity(tx_id, vehicle_data)
    print(f"Data integrity verified: {is_valid}")
    
    # Get vehicle history
    history = blockchain.get_vehicle_history('AETHER_001')
    print(f"Vehicle history: {len(history)} transactions found")