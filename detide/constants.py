from pytides2 import constituent

RESAMPLE = 60

SHORT = [
    constituent._N2,
    constituent._K2,
    constituent._S2,
    constituent._M2,
    constituent._2N2,  # Semi-diurnal (twice daily)
    constituent._K1,
    constituent._O1,
    constituent._P1,
    constituent._Q1,
    constituent._J1,
    constituent._S1,  # Diurnal (once daily)
    constituent._Mf,
    constituent._Mm,
    constituent._MSF,
    constituent._Sa,
    constituent._Ssa,  # Long period (fortnightly to annual)
    constituent._M4,
    constituent._MS4,
    constituent._M6,
    constituent._MN4,  # Short period (higher harmonics)
]

FULL = [
    constituent._M2,
    constituent._S2,
    constituent._N2,
    constituent._K2,
    constituent._2N2,
    constituent._L2,
    constituent._T2,
    constituent._R2,
    constituent._nu2,
    constituent._mu2,
    constituent._lambda2,  # Semi-diurnal (twice daily)
    constituent._K1,
    constituent._O1,
    constituent._P1,
    constituent._Q1,
    constituent._J1,
    constituent._S1,  # Diurnal (once daily)
    constituent._Mf,
    constituent._Mm,
    constituent._MSF,
    constituent._Sa,
    constituent._Ssa, # Long period (fortnightly to annual)
    constituent._M4,   
    constituent._MS4,
    constituent._M6,
    constituent._MN4,
    constituent._S4,
    constituent._M8,
    constituent._M3,  # Short period (higher harmonics)
]

NOAA = constituent.noaa

EXTENDED = [
    c for c in constituent.extended
    if c not in (constituent._Sa, constituent._Ssa)
]
