"""VERSION v1.0. Fictional formations, deterministic seed, no copied performance art."""
import math,random
SEED=20261110
def positions(count=120,phase=0.,seed=SEED):
    if count<1:raise ValueError('positive count required')
    rng=random.Random(seed);out=[]
    for i in range(count):
        t=2*math.pi*i/count
        out.append((30*math.cos(t),0.2*rng.uniform(-1,1),30+15*math.sin(t+phase)))
    return out
if __name__=='__main__':
    assert positions()==positions()
    assert len(positions())==120
    print('FORMATION_SELFTEST PASS')
