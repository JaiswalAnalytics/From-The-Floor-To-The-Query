"""Generates a synthetic dataset modeled on a building-materials retail store.
50 SKUs, 180 days of sales ending 2026-09-30. Not real store data."""
import random, csv, datetime as dt
random.seed(7)
AS_OF = dt.date(2026, 9, 30)
cats = {
 'Cement & Putty': (['OPC 53 Grade 50kg','PPC 50kg','White Cement 5kg','Wall Putty 20kg','Block Jointing Mortar 25kg','Waterproofing Compound 5kg'], (210,540)),
 'Steel': (['TMT 8mm Bundle','TMT 10mm Bundle','TMT 12mm Bundle','TMT 16mm Bundle','Binding Wire 25kg','MS Angle 25mm'], (1500,9500)),
 'Tiles': (['Vitrified 2x2 White','Vitrified 2x2 Beige','Floor Tile 1x1 Matt','Wall Tile 1x2 Glossy','Parking Tile 1x1','Vitrified 2x4 Marble','Bathroom Tile 1x1.5','Border Tile Gold'], (260,1150)),
 'Adhesive & Grout': (['Tile Adhesive 20kg','Tile Adhesive 5kg','Epoxy Grout 1kg','Grout Powder 1kg','Tile Spacer Pack'], (60,780)),
 'Paint': (['Exterior Emulsion 20L','Interior Emulsion 10L','Primer White 20L','Enamel Black 1L','Enamel Red 1L','Distemper 20kg','Wood Polish 1L','Texture Paint 20kg'], (180,4300)),
 'Plumbing': (['CPVC Pipe 1in','PVC Pipe 4in','GI Elbow 1in','Ball Valve 1/2in','Water Tank 1000L','Solvent Cement 500ml'], (45,6200)),
 'Electrical': (['Wire 1.5mm Coil','Wire 2.5mm Coil','MCB 16A','Switch Plate 6M','LED Panel 15W'], (110,2300)),
 'Sanitary': (['Wash Basin White','Western Toilet Seat','Health Faucet','Bathroom Mirror'], (280,3100)),
 'Hardware': (['Door Lock Set','Hinge 4in'], (90,650)),
}
dead = {'Border Tile Gold':(170,60),'Vitrified 2x4 Marble':(130,90),'Parking Tile 1x1':(115,140),'Enamel Red 1L':(105,45),
        'Texture Paint 20kg':(150,25),'Distemper 20kg':(122,30),'Epoxy Grout 1kg':(98,36),'Water Tank 1000L':(160,7),
        'Bathroom Mirror':(140,22),'Health Faucet':(101,40),'MS Angle 25mm':(108,180)}   # name:(days since last sale, stock qty)
slow = {'Wall Tile 1x2 Glossy','Vitrified 2x2 Beige','Wood Polish 1L','Hinge 4in'}
COST = {'MS Angle 25mm':720,'Binding Wire 25kg':1850,'Enamel Red 1L':420,'Enamel Black 1L':400,'Wood Polish 1L':380,
 'Distemper 20kg':1350,'Texture Paint 20kg':1900,'Exterior Emulsion 20L':3900,'Interior Emulsion 10L':2600,'Primer White 20L':2400,
 'Water Tank 1000L':5800,'Epoxy Grout 1kg':640,'Health Faucet':480,'Bathroom Mirror':1450,'Vitrified 2x4 Marble':950,
 'Border Tile Gold':620,'Parking Tile 1x1':380,'Tile Spacer Pack':45,'MCB 16A':185,'Switch Plate 6M':160,'Hinge 4in':55,
 'GI Elbow 1in':35,'Ball Valve 1/2in':140,'Solvent Cement 500ml':110,'CPVC Pipe 1in':190,'PVC Pipe 4in':520,'Grout Powder 1kg':60,
 'Tile Adhesive 5kg':185,'Tile Adhesive 20kg':560,'LED Panel 15W':240,'Door Lock Set':650,'Wire 1.5mm Coil':1300,'Wire 2.5mm Coil':2100,
 'Distemper 20kg':1350,'Wall Putty 20kg':520,'Block Jointing Mortar 25kg':260,'Waterproofing Compound 5kg':480,'White Cement 5kg':210}
products, sales, n = [], [], 0
for cat,(names,(lo,hi)) in cats.items():
    for nm in names:
        n += 1; sku = f'SKU{n:03d}'
        cost = COST.get(nm) or (round(random.uniform(lo,hi)/5)*5 or 5)
        if nm in dead: last, qty = dead[nm]; rate = random.uniform(.3,.8)
        elif nm in slow: last, qty = random.randint(48,78), random.randint(18,40); rate = random.uniform(.2,.4)
        else: last, qty = 0, None; rate = random.uniform(1.2,7)
        end = AS_OF - dt.timedelta(days=last)
        tot = 0
        for d in range(180):
            day = AS_OF - dt.timedelta(days=179-d)
            if day > end: continue
            q = sum(random.random() < rate/3 for _ in range(3))
            if day == end and q == 0: q = 1
            if q: sales.append((sku, day.isoformat(), q)); tot += q
        if qty is None: qty = max(6, round(rate*random.randint(9,26)))
        products.append((sku, nm, cat, cost, qty))
with open('data/products.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['sku','product_name','category','cost_price','stock_qty']); w.writerows(products)
with open('data/sales.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['sku','sale_date','qty']); w.writerows(sales)
print(len(products), 'products,', len(sales), 'sales rows')
