"""
Convert the MEME motifs into single files containg one PWM each

IN: MEME file with several motifs
OUT: several PWM files , the names are in the form of 315_motif.71_Limb_E14.5_H3K4me276_0.552_5.148606e-96_10.motif
"""

from sys import argv

def load_motifsSpecial(filename):
    file=open(filename)
    seq=file.read().split("MOTIF")
    seq=seq[1:]
    motifs={}
    infos={}
    pseudocount=0.001
    for s in range(len(seq)):
        t=seq[s].strip().split("\n")
        motifs[t[0]]=t[2:]
        infos[t[0]]=t[:2]
    for m in motifs:
        tdict={'A':[],'C':[],'G':[],'T':[]}
        for pos in range(len(motifs[m])):
            tmp=motifs[m][pos].strip().split("\t")
            tdict['A']+=[(float(tmp[0])+pseudocount)/(1.0+4*pseudocount)]
            tdict['C']+=[(float(tmp[1])+pseudocount)/(1.0+4*pseudocount)]
            tdict['G']+=[(float(tmp[2])+pseudocount)/(1.0+4*pseudocount)]
            tdict['T']+=[(float(tmp[3])+pseudocount)/(1.0+4*pseudocount)]
            #tdict['E']+=[float(tmp[4])]
        motifs[m]=tdict
    
    return motifs,infos


def main():
	inmeme=argv[1]
	outputdir=argv[2]
	
	motifs,infos=load_motifsSpecial(inmeme)
	motifnames=sorted(motifs.keys())
	klength=0
	count=0
	for motif in motifnames:
		klength=len(motifs[motif]['A'])
		pwm=motifs[motif]
		#print motif,klength
		newname=str(count)+"_motif."+motif+"_"+str(klength)+".motif"
		count+=1
		print newname
		target=open(outputdir+'/'+newname,'w')
		for i in range(klength):
			line=str(pwm['A'][i])+'\t'+str(pwm['C'][i])+'\t'+str(pwm['G'][i])+'\t'+str(pwm['T'][i])+'\n'
			target.write(line)
		target.close()

	return

if __name__=="__main__":
	main()