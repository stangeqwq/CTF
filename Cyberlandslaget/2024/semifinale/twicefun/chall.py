from Crypto.Util.number import getPrime, isPrime, bytes_to_long

flagg = b"flag{fake_flagg}"
e = 65537

p = getPrime(1024)

q = 2*p+1

while not isPrime(q):
    q+=2

n = p*p*q


ct = pow(bytes_to_long(flagg), e, n)

print(f"{n=}")
print(f"{e=}")
print(f"{ct=}")
print(f"{p=}")
print(f"{q=}")
# test 
# p = 161958057002177785533532537270350808812372862511718038162751489984717732609850870591672781976093869528627261313627660165764962225683407025122410138934385379223018444978398324911923096107862957370463145757941232456242667370481814292026739935175092702196537125268107185493890961306261363350782573845670293215687
# q = 323916114004355571067065074540701617624745725023436076325502979969435465219701741183345563952187739057254522627255320331529924451366814050244820277868770758446036889956796649823846192215725914740926291515882464912485334740963628584053479870350185404393074250536214370987781922612522726701565147691340586432151

# my solve.py solution (IT WORKS)
# p = 161958057002177785533532537270350808812372862511718038162751489984717732609850870591672781976093869528627261313627660165764962225683407025122410138934385379223018444978398324911923096107862957370463145757941232456242667370481814292026739935175092702196537125268107185493890961306261363350782573845670293215687
# q = 323916114004355571067065074540701617624745725023436076325502979969435465219701741183345563952187739057254522627255320331529924451366814050244820277868770758446036889956796649823846192215725914740926291515882464912485334740963628584053479870350185404393074250536214370987781922612522726701565147691340586432151
'''
n=8496453197600393771349140860945008171508003756066685002547083293898203155716100171534807253620273799823877505248674827308382347860398638761333491553156412989439814977658862395284244064512695683818504797918799546745900345335077797112914785215605937565545715297765824237487992843670053209669018307123345921101178280481719414429664380430482196408564309273655860457184004876026633133099500720034744237005523049137581285871372437707727534323319326823722292850923489704197430728510533219939852090205805305838194672026945860344422878420659214650594243464454540661561988744842603314851866483263955877940964922540851814330360450948005448554756325028784244705956494304359220260546239898287344026637783604892302406994838755988859973239702781216326758955759175043784422002143102422430564372001347949518141766080519053228915728458026483086676194321044736691485331309575802069022037301078312088758172488665968370018683429309918623379785319
e=65537
ct=2685801208577838217777325918757915037541938912139000783970157159184776473528654091330401273558260617373611097331521489941353148960049053666844097270925762642367060023996722783991045521024513706107695150275233205990006254431599950256010691983185576673776772275964656888126366954500317403300233830911822961523421151955432057326748660577876314626205585282533299465228953472870693925809731887960469990993905533300782668294857336508040522062227237720064441502878478089599632205716177954221028910070952700075516527391677532965567597425432982360652694193113943736980375509215373512538862543756777283349261070318084285521291154949529850137298202472731158540643592269887332301204835223246116475476556736118058797658321576378115976298806264672425159566223458811992554539595491949483653391981869523809657407415203588923161966130898659717811423642138406599575864755631271807470099021913002798665502117524108061680647220508511167273589409

'''