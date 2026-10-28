# 04 — Blueprint de Portage vers Java Orienté Objet (Cursus ASEDS INPT)

Ce document explique comment chaque module du moteur Python (`engine/`) a été conçu pour se traduire directement en **Java Orienté Objet (Java 17/21)** sans aucune réécriture algorithmique.

---

## 1. Correspondance des Structures de Données (`@dataclass(frozen=True)` $\leftrightarrow$ `record` Java)

En Python (`engine/`), toutes nos structures de résultats sont immuables (`@dataclass(frozen=True)`).
En Java moderne (Java 16+), elles se traduisent ligne pour ligne en **`record`** immuables :

### Exemple : `OctetAnalysis`
**Python ([`engine/ipv4_math.py`](file:///C:/Users/lenovo/Desktop/laformatik/ipv4-subnet-toolkit/v1.2.0/engine/ipv4_math.py)) :**
```python
@dataclass(frozen=True)
class OctetAnalysis:
    value: int
    binary_str: str
    hex_str: str
    is_valid_mask_octet: bool
    ones_complement: int
    ones_complement_binary: str
    block_size: int
```

**Java (Équivalent direct) :**
```java
public record OctetAnalysis(
    int value,
    String binaryStr,
    String hexStr,
    boolean isValidMaskOctet,
    int onesComplement,
    String onesComplementBinary,
    int blockSize
) {}
```

---

## 2. Pièges Binaires 32 bits entre Python et Java (`int` signé vs `long`)

### Le piège du type `int` en Java
- En **Python**, `int` a une précision arbitraire : `0xFFFFFFFF` vaut `+4294967295`.
- En **Java**, `int` est signé sur 32 bits (`-2^31` à `2^31 - 1`) : `0xFFFFFFFF` vaut `-1`, et l'opérateur `>>` est un décalage arithmétique (qui propage le bit de signe `1` à gauche !).

### Règles d'Or pour le portage Java de `IPv4MathEngine` :
1. Utiliser le type **`long` (64 bits)** en Java pour stocker les adresses IPv4 32 bits non signées, ou utiliser l'opérateur de décalage logique non signé **`>>>`** :
   ```java
   long maskInt = (cidr > 0) ? ((0xFFFFFFFFL << (32 - cidr)) & 0xFFFFFFFFL) : 0L;
   long wildcardInt = (~maskInt) & 0xFFFFFFFFL;
   long networkInt = ipInt & maskInt;
   long hostIdInt = ipInt & wildcardInt;
   long broadcastInt = networkInt | wildcardInt;
   ```
2. Pour le **Checksum 16 bits (`DrillsSolver.solveChecksum`)** :
   ```java
   int carried = rawSum;
   while (carried > 0xFFFF) {
       carried = (carried & 0xFFFF) + (carried >>> 16);
   }
   int checksum = (~carried) & 0xFFFF;
   ```

---

## 3. Architecture MVC / MVP pour un portage JavaFX ou Swing

Grâce au découplage strict réalisé en `v1.2.0` :
- **Package `ma.inpt.aseds.subnet.engine`** : Contient `IPv4MathEngine`, `VlsmSolver`, `DrillsSolver`, `TipsAndStreakManager` (100% Java standard, testable avec **JUnit 5**).
- **Package `ma.inpt.aseds.subnet.ui`** : Contient les vues JavaFX (avec fichiers CSS équivalents à notre `ui/themes.py` QSS !) ou Swing FlatLaf.
