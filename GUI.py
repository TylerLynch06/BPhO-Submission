import customtkinter as ctk
import MiscMath1
from MiscMath1 import *


class GUIHandler:

    def __init__(self,window,graph):
        self.ongoingAnimation=False
        self.modelSwitches=[]
        self.previousModelId=0
        self.verticesWarning=False
        self.verletStepValue=0.01
        self.verletBounceValue = 5
        self.sliderInput=True
        self.window = window
        self.graph = graph

        ##Most inefficient code ever designed
        ##When tab is swapped, update data only once, if in info view, values cannot be changd, therefore model info will not change
        self.tabMaster= ctk.CTkTabview(self.window,width=700,height=1000,command=self.updateModelInfo)
        self.tabMaster.pack(side=ctk.LEFT,padx=20,pady=10,anchor="nw")

        self.tabMaster.add("Control Centre")
        self.tabMaster.add("Model Information")

    def load(self):

        self.constructControlCentre()
        self.constructAnalyticModelInfo()
        self.graph.idle(2)

    def constructControlCentre(self):
        self.sliderEntryToggle = ctk.CTkOptionMenu(self.tabMaster.tab("Control Centre"), values=["Slider Input", "Entry Input"],
                                         command=self.updateInputMethod)
        self.sliderEntryToggle.pack(side=ctk.TOP,anchor="w",padx=10,pady=10)
        self.superInputLocation = ctk.CTkFrame(self.tabMaster.tab("Control Centre"))
        self.superInputLocation.pack(side=ctk.TOP,padx=10,pady=10)
        self.constructVariableInputs()

        #self.angleLimit = ctk.CTkLabel(self.limits,text="90")
        #self.angleLimit.pack(side=ctk.TOP,padx=10,pady=10)

        self.graph.GUI = self
        self.graph.update(1)
        self.graph.setOfPlots=self.graph.setPoints()

        self.animationModelMaster = ctk.CTkFrame(self.tabMaster.tab("Control Centre"))
        self.animationModelMaster.pack(side=ctk.TOP)
        
        self.modelMaster = ctk.CTkFrame(self.animationModelMaster,fg_color="#333333",height=450)
        self.modelMaster.pack(side=ctk.LEFT,pady=10,padx=10,expand=True,fill=ctk.BOTH)
        self.modelLabel = ctk.CTkLabel(self.modelMaster,text="Model Select",font=("Roboto",25,'bold'))
        self.modelLabel.pack(side=ctk.TOP)
        self.modelCombo = ctk.CTkComboBox(self.modelMaster,corner_radius=20, font=("Roboto",25),values=["Analytic Parabolas",
                                                                                                        "Range Time Curve",
                                                                                                        "Verlet Bouncing Ball",
                                                                                                        "Non-linear Resistance",
                                                                                                        "Parametric t-model"],width=300)
        self.modelCombo.pack(side=ctk.TOP,anchor="w",pady=10,padx=10)
        self.modelButton =  ctk.CTkButton(self.modelMaster,text="Apply Model",font=("Roboto",25),command=self.updateModel)
        self.modelButton.pack(side=ctk.TOP,pady=10,padx=10)
        self.airResistanceSwitch = ctk.CTkSwitch(self.modelMaster,text="Air Resistance",font=("Roboto",25),onvalue=True,offvalue=False,command=self.applyAirResistance)
        self.airResistanceSwitch.pack(side=ctk.TOP,padx=10,pady=10)

        self.animationFrame = ctk.CTkFrame(self.animationModelMaster,height=450)
        self.animationFrame.pack(side=ctk.LEFT,padx=10,pady=10,expand=True,fill=ctk.BOTH)

        self.animationLabel=ctk.CTkLabel(self.animationFrame,text="Animation",font=("Roboto",25,'bold'))
        self.animationButtonMaster=ctk.CTkFrame(self.animationFrame,fg_color="#333333")
        self.saveAnimationButton = ctk.CTkButton(self.animationButtonMaster,text="Save Animation", font=("Roboto",25),command=self.toggleAnimation,hover=True,state="disabled")
        self.replayAnimationButton = ctk.CTkButton(self.animationButtonMaster,text="Restart Animation", font=("Roboto",25),command=self.resetAnimation,hover=True,state="disabled")
        self.playAnimationButton = ctk.CTkButton(self.animationButtonMaster,text="Toggle Animation", font=("Roboto",25),command=self.toggleAnimation,hover=True)
        self.PPFFrame = ctk.CTkFrame(self.animationFrame,fg_color="#333333")
        self.PPFLabel = ctk.CTkLabel(self.PPFFrame,text="Points Per Frame: 30",font=("Roboto",25))
        self.PPFInput = ctk.CTkSlider(self.PPFFrame,from_=1,to=500,command=self.updateInputs,width=100)
        self.PPFInput.set(30)
        self.animationLabel.pack(side=ctk.TOP)
        self.animationButtonMaster.pack(side=ctk.TOP)
        self.saveAnimationButton.pack(side=ctk.TOP,padx=10,pady=10,anchor="w")
        self.replayAnimationButton.pack(side=ctk.TOP,padx=10,pady=10,anchor="w")
        self.playAnimationButton.pack(side=ctk.TOP,padx=10,pady=10,anchor="w")
        self.PPFFrame.pack(side=ctk.TOP)
        self.PPFLabel.pack(side=ctk.LEFT)
        self.PPFInput.pack(side=ctk.LEFT)
       
        self.extraControlLocation = ctk.CTkFrame(self.tabMaster.tab("Control Centre"))
        self.extraControlLocation.pack(side=ctk.TOP,anchor="n",pady=10)
        ##self.graph.setOfPlots=self.graph.setPoints()
        self.applyAnalyticModel()

        self.bottomMaster = ctk.CTkFrame(self.window,fg_color="#1F1F29")
        self.bottomMaster.pack(side=ctk.BOTTOM,anchor="e")
        self.exitButton = ctk.CTkButton(self.bottomMaster, text="Quit",font=("Roboto",40), command=self.window.destroy)
        self.exitButton.pack(pady=20,padx=20,side=ctk.RIGHT)
        self.pauseLabel = ctk.CTkLabel(self.bottomMaster, text="Press 'P' to pause", font=("Roboto",25))
        self.pauseLabel.pack(pady=20,padx=30,side=ctk.RIGHT,)
        self.updateInputs()
        self.graph.idle(3)
       
    def constructVariableInputs(self):
        self.graph.idle(30)
        try:
            if self.superInputs: self.superInputs.destroy()
        except:
            pass

        if self.sliderInput==True: inputIndex=0
        else: inputIndex=1

        self.superInputs = ctk.CTkFrame(self.superInputLocation)
        self.superInputs.pack(padx=10)

        self.Inputs = ctk.CTkFrame(self.superInputs)
        self.Inputs.pack(side=ctk.LEFT,anchor="nw",padx=10,pady=10)

        self.valueLabel = ctk.CTkLabel(self.Inputs,text="Values",font=("Roboto",25,'bold'))
        self.valueLabel.pack(side=ctk.TOP)

        self.velocityMaster = ctk.CTkFrame(self.Inputs)
        self.velocityMaster.pack(side=ctk.TOP,anchor="e",pady=10,padx=10)
        velocityInputs = [ctk.CTkSlider(master=self.velocityMaster,from_=1,to=100,command=self.updateInputs),
                          ctk.CTkEntry(self.velocityMaster,placeholder_text="Enter Value")]
        self.velocityInput = velocityInputs[inputIndex]
        velocityInputs[0].set(30)
        self.velocityText = ctk.CTkLabel(master=self.velocityMaster,text="Velocity (ms⁻¹): ", font=("Roboto",25))
        self.velocityInput.pack(side=ctk.RIGHT)
        self.velocityText.pack(side=ctk.RIGHT,padx=10)
        self.heightMaster = ctk.CTkFrame(self.Inputs)
        self.heightMaster.pack(side=ctk.TOP,anchor="e",pady=10,padx=10)
        heightInputs = [ctk.CTkSlider(master=self.heightMaster,from_=0,to=100,command=self.updateInputs),
                        ctk.CTkEntry(self.heightMaster,placeholder_text="Enter Value")]
        self.heightInput = heightInputs[inputIndex]
        self.heightText = ctk.CTkLabel(master=self.heightMaster,text="Launch Height (m): ", font=("Roboto",25))
        self.heightInput.pack(side=ctk.RIGHT)
        self.heightText.pack(side=ctk.RIGHT,padx=10)

        self.angleMaster = ctk.CTkFrame(self.Inputs)
        self.angleMaster.pack(side=ctk.TOP,anchor="e",pady=10,padx=10)
        angleInputs = [ctk.CTkSlider(master=self.angleMaster,from_=-90,to=90,command=self.updateInputs),
                       ctk.CTkEntry(self.angleMaster,placeholder_text="Enter Value")]
        angleInputs[0].set(45)
        self.angleInput = angleInputs[inputIndex]
        self.angleText = ctk.CTkLabel(master=self.angleMaster,text="Launch Angle (°): ", font=("Roboto",25))
        self.angleInput.pack(side=ctk.RIGHT)
        self.angleText.pack(side=ctk.RIGHT,padx=10)

        if self.sliderInput:
            self.limits = ctk.CTkFrame(self.superInputs)
            self.limits.pack(side=ctk.TOP,anchor="nw",padx=10,pady=9)

            self.limitLabel = ctk.CTkLabel(self.limits,text="Limits",font=("Roboto",25,'bold'))
            self.limitLabel.pack(side=ctk.TOP)

            self.velocityLimit = ctk.CTkEntry(self.limits,placeholder_text="100")
            self.velocityLimit.pack(side=ctk.TOP,padx=10,pady=11)

            self.heightLimit = ctk.CTkEntry(self.limits,placeholder_text="100")
            self.heightLimit.pack(side=ctk.TOP,padx=10,pady=10)

            self.applyLimitButton = ctk.CTkButton(self.limits,text="Apply Limits",font=("Roboto",25),command=self.updateLimits)
            self.applyLimitButton.pack(side=ctk.TOP,padx=10,pady=10)
            self.updateInputs()
        else: self.limits.destroy()

    def constructAnalyticModelInfo(self):
        i=0
        self.modelInfoFrame=ctk.CTkFrame(master=self.tabMaster.tab("Model Information"))
        self.modelInfoFrame.pack(side=ctk.TOP,padx=10,pady=10)
        self.parabolaLabels=[]
        for plot in (self.graph.particle.parabolas+[self.graph.particle.boundingParabola]):
            if i%2==0:
                doubleTextMaster= ctk.CTkFrame(self.modelInfoFrame,fg_color="#1F1F29",width=400,height=500,corner_radius=20)
                doubleTextMaster.pack(side=ctk.TOP,padx=10,pady=5)
            newTextMaster = ctk.CTkFrame(master=doubleTextMaster,fg_color="#333333",width=200,height=500,corner_radius=20)
            newTextMaster.pack(side=ctk.LEFT,anchor="n",pady=10,padx=10,expand=1, fill=ctk.BOTH)
            i+=1
            newLabel = ctk.CTkLabel(newTextMaster,text=f"{plot.name}",font=("Roboto",25,'bold'),width=200)
            newLabel.pack(side=ctk.TOP,anchor="w",pady=10,padx=10)
            lines=[]
            for line in plot.text: 
                newLine = ctk.CTkLabel(newTextMaster,text=f"{line}",font=("Roboto",20),width=200)
                newLine.pack(side=ctk.TOP,pady=3,padx=3)
                lines.append(newLine)
            self.parabolaLabels.append(lines)

    def constructRangeModelInfo(self):
        i=0
        self.modelInfoFrame=ctk.CTkFrame(master=self.tabMaster.tab("Model Information"),fg_color="#333333",width=800,height=500,corner_radius=20)
        self.modelInfoFrame.pack(side=ctk.TOP,padx=10,pady=10,fill=ctk.BOTH)
        info = self.graph.particle.rangeParticleInfo
        self.rangeModelData = []
        index=0
        ##print(f"Info: \n{info}\n")
        for angle in info:
            if i%2==0:
                doubleTextMaster= ctk.CTkFrame(self.modelInfoFrame,fg_color="#1F1F29",width=400,height=500,corner_radius=20)
                doubleTextMaster.pack(side=ctk.TOP,padx=10,pady=5)
            newTextMaster = ctk.CTkFrame(master=doubleTextMaster,fg_color="#333333",width=200,height=500,corner_radius=20)
            newTextMaster.pack(side=ctk.LEFT,anchor="n",pady=10,padx=10,expand=1, fill=ctk.BOTH)
            i+=1
            newLabel = ctk.CTkLabel(newTextMaster,text=f"{angle[0]}°",font=("Roboto",25,'bold'),width=200)
            newLabel.pack(side=ctk.TOP,anchor="w",pady=10,padx=10)
            if index==7:
                self.customAngleRangeLabel = newLabel
            if len(angle)==1 and index!=7:
                newLine = ctk.CTkLabel(newTextMaster,text="No Turning Points",font=("Roboto",20),width=200)
                newLine.pack(side=ctk.TOP,pady=3,padx=3)
                self.rangeModelData.append(None)
            elif index == 7:
                tp1 = ctk.CTkLabel(newTextMaster,text=f"Maxima: nan",font=("Roboto",20),width=200)
                tp1.pack(side=ctk.TOP,pady=3,padx=3)
                tp2 = ctk.CTkLabel(newTextMaster,text=f"Minima: nan",font=("Roboto",20),width=200)
                tp2.pack(side=ctk.TOP,pady=3,padx=3)
                self.rangeModelData.append((tp1,tp2))
            else:
                tp1 = ctk.CTkLabel(newTextMaster,text=f"Maxima: ({MiscMath1.sf(angle[1][0][0])},{MiscMath1.sf(angle[1][0][1])})",font=("Roboto",20),width=200)
                tp1.pack(side=ctk.TOP,pady=3,padx=3)
                tp2 = ctk.CTkLabel(newTextMaster,text=f"Minima: ({MiscMath1.sf(angle[1][1][0])},{MiscMath1.sf(angle[1][1][1])})",font=("Roboto",20),width=200)
                tp2.pack(side=ctk.TOP,pady=3,padx=3)
                self.rangeModelData.append((tp1,tp2))
            index+=1
        
    def constructVerletModelInfo(self):
        self.modelInfoFrame=ctk.CTkFrame(master=self.tabMaster.tab("Model Information"),fg_color="#333333",width=800,height=500,corner_radius=20)
        self.modelInfoFrame.pack(side=ctk.TOP,padx=10,pady=10,fill=ctk.BOTH)

        self.verletInfoTitle = ctk.CTkLabel(self.modelInfoFrame,text=f"Verlet Ball",font=("Roboto",25,'bold'),width=800)
        self.verletInfoTitle.pack(side=ctk.TOP)
        self.verletAirTimeLabel = ctk.CTkLabel(self.modelInfoFrame,text=f"Air Time (s): {MiscMath1.sf(self.graph.particle.time)}",font=("Roboto",20),width=800)
        self.verletAirTimeLabel.pack(side=ctk.TOP)
        self.verletDisplacementLabel=ctk.CTkLabel(self.modelInfoFrame,text=f"Displacement (m): {MiscMath1.sf(self.graph.particle.totalDisplacement)}",font=("Roboto",20),width=800)
        self.verletDisplacementLabel.pack(side=ctk.TOP)
        
    def constructParametricModelInfo(self):
        self.modelInfoFrame=ctk.CTkFrame(master=self.tabMaster.tab("Model Information"),fg_color="#333333",width=800,height=500,corner_radius=20)
        self.modelInfoFrame.pack(side=ctk.TOP,padx=10,pady=10,fill=ctk.BOTH)

        self.parametricInfoTitle = ctk.CTkLabel(self.modelInfoFrame,text=f"Parametric Projectile",font=("Roboto",25,'bold'),width=800)
        self.parametricInfoTitle.pack(side=ctk.TOP)
        textMaster= ctk.CTkFrame(self.modelInfoFrame,fg_color="#333333",width=300,height=500,corner_radius=20)
        textMaster.pack(side=ctk.TOP,padx=10,pady=5)
        self.impactTimeLabel = ctk.CTkLabel(textMaster,text="Impact Time: ",font=("Roboto",25))
        self.impactTimeLabel.pack(side=ctk.TOP,padx=10,pady=5)

    def updateModelInfo(self):

        self.graph.idle()
        if self.previousModelId==0:
            ##print(self.graph.particle.parabolas[0].text[0])
            for (label,parabola) in zip(self.parabolaLabels,self.graph.particle.parabolas+[self.graph.particle.boundingParabola]):
                for i,line in enumerate(label):
                    line.configure(text=parabola.text[i])
        if self.previousModelId==1:
            index=0
            ##print(self.rangeModelData)
            info = self.graph.particle.rangeParticleInfo
            ##print(f"Info: \n{info}\n")
            self.customAngleRangeLabel.configure(text=f"{MiscMath1.sf(info[-1][0])}°")
            for angle in self.rangeModelData:
                if angle!=None:
                    try:
                        angle[0].configure(text=f"Maxima: ({MiscMath1.sf(self.graph.particle.minMaximaPoints[index][0])},{MiscMath1.sf(self.graph.particle.minMaximaPoints[index][1])})")
                        index+=1
                        angle[1].configure(text=f"Minima: ({MiscMath1.sf(self.graph.particle.minMaximaPoints[index][0])},{MiscMath1.sf(self.graph.particle.minMaximaPoints[index][1])})")
                    except: 
                        angle[0].configure(text=f"Maxima: nan")
                        index+=1
                        angle[1].configure(text=f"Minima: nan")
        
                index+=1
        if self.previousModelId==2:
            self.verletAirTimeLabel.configure(text=f"Air Time (s): {MiscMath1.sf(self.graph.particle.time)}")
            self.verletDisplacementLabel.configure(text=f"Displacement (m): {MiscMath1.sf(self.graph.particle.totalDisplacement)}")
        if self.previousModelId==4:
            self.impactTimeLabel.configure(text=f"Impact Time (s): {MiscMath1.sf(self.graph.particle.impactTime)}")

    def updateInputs(self,value=None):
        self.graph.idle(3)
        ##print("updating")
        try:
            self.velocityText.configure(text=f"Velocity (ms⁻¹): {int(self.velocityInput.get())}")
            self.angleText.configure(text=f"Angle (°): {int(self.angleInput.get())}")
            self.heightText.configure(text=f"Launch height (m): {int(self.heightInput.get())}")
        except: pass
        try:
            self.PPFLabel.configure(text=f"Points Per Frame: {int(self.PPFInput.get())}")
        except: pass
        if self.previousModelId==2:
            ##print("Updating")
            self.updateVerletControls()
            if self.graph.particle.time//self.graph.particle.step>30000 and not self.verticesWarning:
                self.verticesWarning=True
                warningLabel=ctk.CTkLabel(self.verletMaster,text="WARNING: Exceeding 30,000 vertices.\nThis is likely to affect performance\nReduce values to improve performance"
                                          ,font=("Roboto",25,"bold")
                                          ,text_color="#FF0000")
                warningLabel.pack(side=ctk.BOTTOM)
            
    def updateLimits(self):
        self.graph.idle(3)
        try:
            vLimit = int(self.velocityLimit.get())
            self.velocityInput.configure(to=vLimit)
            ##If v is greater than limit, let v = limit
            if vLimit<self.velocityInput.get(): self.velocityInput.set(vLimit)
        except: pass
        try:
            hLimit = int(self.heightLimit.get())
            self.heightInput.configure(to=hLimit)
            if hLimit<self.heightInput.get(): self.heightInput.set(hLimit)
        except: pass
        ##So value remains constant when limit greater than current value
        self.calibrateInputText()
        self.updateInputs()
        #self.velocityInput.pack(side=ctk.LEFT,padx=10)

    def updateModel(self): 
        ##print("updated")
        self.graph.idle(20)
        selectedModel=self.modelCombo.get()
        self.verticesWarning=False
        if self.graph.animating:
            self.replayAnimationButton.configure(state="disabled")
            self.saveAnimationButton.configure(state="disabled")
        models = ["Analytic Parabolas","Range Time Curve","Verlet Bouncing Ball","Non-linear Resistance","Parametric t-model"]
        if models[self.previousModelId]!=selectedModel:
            ##print(selectedModel)
            for i in range(len(models)):
                if selectedModel==models[i]:
                    self.graph.loadNewModel(i)
                    self.previousModelId=i
                    break
            ##print("Stage 1: ",i)
            if i == 1: 
                self.playAnimationButton.configure(state="disabled")
                self.airResistanceSwitch.select()
                self.airResistanceSwitch.toggle()
                self.airResistanceSwitch.configure(state="disabled")              
            else: 
                self.playAnimationButton.configure(state="normal")
                self.airResistanceSwitch.configure(state="normal")
            if i==0: 
                self.modelInfoFrame.destroy()
                self.constructAnalyticModelInfo()
                self.removeToggledModels()
                self.applyAnalyticModel()

            elif i==1:
                self.modelInfoFrame.destroy()
                self.constructRangeModelInfo()
                self.removeToggledModels()
                
            elif i==2:
                self.modelInfoFrame.destroy()
                self.constructVerletModelInfo()
                self.removeToggledModels()
                self.applyVerletControls()

            elif i==4:
                self.modelInfoFrame.destroy()
                self.constructParametricModelInfo()
                self.removeToggledModels()
                self.applyParametricControls()

            if i==5:
                self.graph._3D=True
                plt.clf()
                ax = fig.add_subplot(projection='3d')

    def updateInputMethod(self,value):
        if value[0]=="E": self.sliderInput=False
        else: self.sliderInput=True
        self.constructVariableInputs()

    def calibrateInputText(self):
        self.velocityInput.set(self.graph.particle.velocity)
        self.heightInput.set(self.graph.particle.launchHeight)

    def resetAnimation(self):
        self.graph.resetAnimation()

    ##Originally planned to have play and exit animation functions seperate, configuring the fucntion of the toggle button to reflect this caused screen jittering, screen jittering still exists however
    def toggleAnimation(self):
        self.graph.idle(6)
        if self.graph.animating: 
            self.saveAnimationButton.configure(state="disabled")
            self.replayAnimationButton.configure(state="disabled")
            self.graph.exitAnimation()

        else: 
            self.saveAnimationButton.configure(state="normal")
            self.replayAnimationButton.configure(state="normal")
            self.graph.beginAnimation()

        ##Return True if data is error free
    def inputVariableProcessing(self):
        self.alertText=""
        try:
            float(self.velocityInput.get())
            if float(self.velocityInput.get())==0:
                self.alertText+=("Velocity must not be 0\n")
                
        except: self.alertText+=("\nInput numeric Launch Velocity")

        try:
            float(self.angleInput.get())
            if float(self.angleInput.get())<-90 or float(self.angleInput.get())>90:
                self.alertText+=("Angle must be a float between -90 and 90\n")
        except: self.alertText+=("\nInput numeric Launch Angle")

        try:
            float(self.heightInput.get())
            if not float(self.heightInput.get())>=0:
                self.alertText+=("Launch Height must be a positive float\n")
        except: self.alertText+=("\nInput numeric Launch Height")
        ##print(self.alertText)
        return self.alertText==""

    def applyAnalyticModel(self):
        self.graph.idle(5)       
        self.modelSwitches=[]
        self.applyAnalyticControls()
        self.currentControlMaster=self.analyticMaster
        i=0
        for switch in (self.graph.particle.parabolas+[self.graph.particle.boundingParabola]):
            newSwitch=ctk.CTkSwitch(self.toggleModelFrame,text=switch.name,font=("Roboto",25),onvalue=True,offvalue=False,command=self.toggleModels)
            ##Set value to on
            if i>0: 
                switch.enabled=False
                newSwitch.deselect()
            else: 
                switch.enabled = True   
                newSwitch.select()
            i+=1
            self.modelSwitches.append(newSwitch)
            newSwitch.pack(side=ctk.TOP,anchor="w",padx=3,pady=3)

    def removeToggledModels(self):
        self.graph.idle(3)
        self.extraControlLocation.configure(fg_color="transparent")
        self.currentControlMaster.destroy()

    def toggleModels(self):
        for i,switch in enumerate(self.modelSwitches[:-1]):
            self.graph.particle.parabolas[i].enabled = switch.get()
        self.graph.particle.boundingParabola.enabled=self.modelSwitches[-1].get()



    def applyAirResistance(self):
        self.graph.airResistance=self.airResistanceSwitch.get()

    def applyAnalyticControls(self):
        self.analyticMaster = ctk.CTkFrame(self.extraControlLocation,fg_color="#333333")
        self.analyticMaster.pack(side=ctk.TOP,padx=20,pady=0)

        self.analyticLabel = ctk.CTkLabel(self.analyticMaster,font=("Roboto",25,'bold'),text="Analytic Model Controls")
        self.analyticLabel.pack(side=ctk.TOP)

        self.toggleModelFrame = ctk.CTkScrollableFrame(self.analyticMaster,fg_color="#2B2B2B")
        self.toggleModelFrame.pack(side=ctk.LEFT,padx=10,pady=10)
        self.pointFrame = ctk.CTkScrollableFrame(self.analyticMaster,fg_color="#2B2B2B",height=100)
        self.pointFrame.pack(side=ctk.RIGHT,padx=10,pady=20)

        self.pointXMaster = ctk.CTkFrame(self.pointFrame)
        self.pointXMaster.pack(side=ctk.TOP,padx=10,pady=5)
        self.pointXEntry = ctk.CTkEntry(self.pointXMaster,placeholder_text="50",font=("Roboto",15),width=50)
        self.pointXEntry.pack(side=ctk.RIGHT)
        self.pointXLabel = ctk.CTkLabel(self.pointXMaster,text="Point X (m):",font=("Roboto",20))
        self.pointXLabel.pack(side=ctk.RIGHT,padx=5)

        self.pointYMaster = ctk.CTkFrame(self.pointFrame)
        self.pointYMaster.pack(side=ctk.TOP,padx=10,pady=5)
        self.pointYEntry = ctk.CTkEntry(self.pointYMaster,placeholder_text="30",font=("Roboto",15),width=50)
        self.pointYEntry.pack(side=ctk.RIGHT)
        self.pointYLabel = ctk.CTkLabel(self.pointYMaster,text="Point Y (m):",font=("Roboto",20))
        self.pointYLabel.pack(side=ctk.RIGHT,padx=5)

        self.pointToggle = ctk.CTkSwitch(self.pointFrame,text="Visible Point",font=("Roboto",20),command=self.toggleVisiblePoint)
        self.pointToggle.pack(padx=5,pady=5)
        self.pointToggle.select()

    def applyVerletControls(self):
        self.verletMaster = ctk.CTkFrame(self.extraControlLocation,fg_color="#333333",width=400)
        self.verletMaster.pack(side=ctk.TOP,padx=20,pady=0)

        self.currentControlMaster=self.verletMaster
        
        self.verletLabel = ctk.CTkLabel(self.verletMaster,font=("Roboto",25,'bold'),text="Verlet Model Controls")
        self.verletLabel.pack(side=ctk.TOP,padx=10,pady=10)

        self.verletEntryFrame = ctk.CTkFrame(self.verletMaster)
        self.verletEntryFrame.pack(side=ctk.TOP,padx=10,pady=10)
        
        self.verletStepMaster = ctk.CTkFrame(self.verletEntryFrame)
        self.verletStepMaster.pack(side=ctk.LEFT,padx=10,pady=10)
        self.verletStepLabel = ctk.CTkLabel(self.verletStepMaster,font=("Roboto",25),text="Time Step (s): ")
        self.verletStepLabel.pack(side=ctk.LEFT,padx=10,pady=10)
        self.verletStepEntry = ctk.CTkEntry(self.verletStepMaster,font=("Roboto",15),placeholder_text="0.01")
        self.verletStepEntry.pack(side=ctk.TOP,padx=10,pady=10)

        self.verletBounceMaster = ctk.CTkFrame(self.verletEntryFrame)
        self.verletBounceMaster.pack(side=ctk.LEFT,padx=20,pady=10)
        self.verletBounceLabel = ctk.CTkLabel(self.verletBounceMaster,font=("Roboto",25),text="Bounces: ")
        self.verletBounceLabel.pack(side=ctk.LEFT,padx=10,pady=10)
        self.verletBounceEntry = ctk.CTkEntry(self.verletBounceMaster,font=("Roboto",20),placeholder_text="5")
        self.verletBounceEntry.pack(side=ctk.LEFT,padx=10,pady=10)
        self.verletModelButton = ctk.CTkButton(self.verletMaster,font=("Roboto",20),text="Apply Verlet Controls",command=self.updateVerletControls)
        self.verletModelButton.pack(side=ctk.TOP,padx=10,pady=10)

        self.verletVerticesLabel=ctk.CTkLabel(self.verletMaster,text=f"Verlet Iterations ≈ {int(self.graph.particle.time//self.graph.particle.step)}",font=("Roboto",20))
        self.verletVerticesLabel.pack(side=ctk.TOP,padx=10,pady=5)

    def updateVerletControls(self):
        try:
            if float(self.verletStepEntry.get())>0:
                self.verletStepValue=float(self.verletStepEntry.get())
        except: pass
        try: 
            if int(self.verletBounceEntry.get())>=0:
                self.verletBounceValue=int(self.verletBounceEntry.get())
        except: pass
        ##No reason for approximation sign. I am lazy and dont want to check if its absolutely correct
        self.graph.particle.getPoints()
        self.verletVerticesLabel.configure(text=f"Verlet Iterations ≈ {int(self.graph.particle.time//self.graph.particle.step)}")

    def applyParametricControls(self):
        self.parametricMaster = ctk.CTkFrame(self.extraControlLocation,fg_color="#333333",width=400)
        self.parametricMaster.pack(side=ctk.TOP,padx=20,pady=0)

        self.currentControlMaster=self.parametricMaster

        self.parametricLabel = ctk.CTkLabel(self.parametricMaster,font=("Roboto",25,'bold'),text="Parametric Model Controls")
        self.parametricLabel.pack(side=ctk.TOP,padx=10,pady=10)

        self.intervalMaster = ctk.CTkFrame(self.parametricMaster,width=300)
        self.intervalMaster.pack(side=ctk.TOP,padx=10,pady=10)
        self.intervalLabel  = ctk.CTkLabel(self.intervalMaster,font=("Roboto",25),text="Δt of Points (s): 1")
        self.intervalLabel.pack(side=ctk.LEFT,padx=10,pady=10)
        self.intervalSlider = ctk.CTkSlider(self.intervalMaster,command=self.updateParametricInterval,from_ = 0.01, to=1)
        self.intervalSlider.pack(side=ctk.LEFT,padx=10,pady=10)
        self.intervalSlider.set(1)

    def updateParametricInterval(self,value=None):
        self.graph.particle.interval = float(self.intervalSlider.get())
        self.intervalLabel.configure(text=f"Δt of Points (s): {MiscMath1.sf(float(self.intervalSlider.get()))}")

    def toggleVisiblePoint(self):
        self.graph.particle.pointToggle=not self.graph.particle.pointToggle

    def realPoint(self):
        try:
            for i in range(1,3):
                self.modelSwitches[i].configure(state="normal")
        except: pass

    def nonRealPoint(self):
        for i in range(1,3):
            self.modelSwitches[i].select()
            self.modelSwitches[i].toggle()
            self.modelSwitches[i].configure(state="disabled")

    def pointZero(self):
        for i in range(1,4):
            self.modelSwitches[i].select()
            self.modelSwitches[i].toggle()
            self.modelSwitches[i].configure(state="disabled")
