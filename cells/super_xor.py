import hashlib

class SuperXor14DMatrix:
    """Động cơ Mê Cung Gương Siêu Khối 14 Chiều kháng bẻ khóa lượng tử"""
    @staticmethod
    def refract_14d(vector, context_tag, dimensions=14):
        masks = []
        for d in range(dimensions):
            h = hashlib.shake_256(f"{context_tag}_axis_{d}".encode()).hexdigest(4)
            masks.append(round(int(h, 16) / 65535.0, 4))
        
        result = list(vector)
        while len(result) < dimensions:
            result.append(0.5)
            
        for i in range(dimensions):
            for m in masks:
                result[i] = round((result[i] + m) % 1.0, 4)
        return result[:dimensions], masks
