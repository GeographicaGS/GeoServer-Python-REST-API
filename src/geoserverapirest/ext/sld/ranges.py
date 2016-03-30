#!/usr/bin/env python
# coding=UTF-8

import random, math, copy

"""
Range and segmentation calculations.
"""


class RuleNames(object):
    """
    This class generates rule names based on given intervals.
    """

    def ruleNames(self, ranges, mono, dual, transform=lambda x: x):
        """
        Takes ranges and generates rule descriptions.

        :param ranges: Ranges to construct the descriptions from.
        :type ranges: List
        :param mono: Mono range sintactic construct.
        :type mono: String
        :param dual: Dual range sintactic construct.
        :type dual: String
        :param transform: Lambda function to modify range values.
        :type transform: lambda
        """

        out = []

        for i in ranges:
            if i[0]==i[1]:
                out.append(mono % transform(i[0]))
            else:
                out.append(dual % (transform(i[0]), transform(i[1])))

        return out
        
    

class Range(object):
    """
    This class implements several methods to calculate ranges and data series
    segmentations.
    """

    def quartileInterval(self, data, intervals, precision):
        """
        Returns quartile intervals. A list of lists of two floats is returned, each one a closed interval.

        :param data: Array of data.
        :type data: List
        :param intervals: Number of intervals.
        :type intervals: Integer
        :param precision: Precision of interval limits, in decimal places.
        :type precision: integer
        :return: A list of lists containing the interval limits as closed intervals on both extremes.
        :rtype: List
        """

        # Prepare data
        data = sorted(data)

        # Interval size
        intSize = int(math.floor(len(data)/intervals))

        # Chop data with intSize. Last interval may be greater if not exactly divisible
        inter = [data[i*intSize:(i+1)*intSize] for i in range(0, intervals-1)]
        inter.append(data[(intervals-1)*intSize:])

        # Retouch intervals so no overlapping values occurs between intervals
        i = 1
        while i<len(inter):
            inter[i] = [k for k in inter[i] if k!=inter[i-1][-1]]

            # Sometimes an empty list is returned            
            if inter[i]==[]:
                del inter[i]
            else:
                i+=1
                        
        # Final closed intervals
        out = [[inter[i][0], inter[i][-1]] for i in range(0, len(inter))]
        
        return out
        

    def equalInterval(self, data, intervals, precision):
        """
        Returns equal intervals. A list of lists of two floats is returned, each a closed interval.

        :param data: Array of data. Just pass [min, max] in case min and max are already know, for example by the function getColumnMinMax in PostGIS submodule.
        :type min: List
        :param intervals: Number of intervals.
        :type intervals: Integer
        :param precision: Precision of interval limits, in decimal places.
        :type precision: Integer
        :return: A list of lists containing the interval limits as closed intervals on both extremes.
        :rtype: List

        .. todo: This function was relocated from SLD and needs proper testing.
        """

        minV = float(min(data))
        maxV = float(max(data))
        
        step = round((maxV-minV)*1.00/intervals, precision)
        precisionStep = math.pow(10, -precision)
        out = []
        
        for i in range(0, intervals):
            out.append([round(minV+(i*step), precision),
                        round(minV+((i+1)*step)-precisionStep, precision)])

        # Redefine upper from last interval
        out[-1][1] = maxV

        return out


    def jenksMiddleInterval(self, data, sideIntervals, middleValue, precision, initialPopulation=50, bestOf=50, \
                      generations=2, bestPopulation=5, mutatedChildrens=2, maxMutations=10):
        """
        Returns Jenks intervals partitioned with a middle value. A list of lists of two floats is returned, each a closed interval.

        :param data: The data sequence.
        :type data: List
        :param intervals: Number of intervals to be computed. Must be less than the different values in the dataset minus one and greater than 0
        :type sideIntervals: Integer
        :param precision: Number of decimals to be used.
        :type precision: Integer
        :return: A list of lists containing the interval limits as closed intervals on both extremes. None if more intervals than data where asked.
        :rtype: List

        .. todo:: create exception, for example to use in this method
        .. todo:: review parameters
        """

        bottomData = [i for i in data if i<middleValue]
        topData =  [i for i in data if i>middleValue]

        bottomRanges = self.jenksInterval(bottomData, sideIntervals, precision)
        topRanges = self.jenksInterval(topData, sideIntervals, precision)

        bottomRanges.append([middleValue, middleValue])
        bottomRanges.extend(topRanges)

        return bottomRanges

        
    def jenksInterval(self, data, intervals, precision, initialPopulation=50, bestOf=50, \
                      generations=2, bestPopulation=5, mutatedChildrens=2, maxMutations=10):
        """
        Returns Jenks intervals. A list of lists of two floats is returned, each a closed interval.

        :param data: The data sequence.
        :type data: List
        :param intervals: Number of intervals to be computed. Must be less than the different values in the dataset minus one and greater than 0
        :type intervals: Integer
        :param precision: Number of decimals to be used.
        :type precision: Integer
        :return: A list of lists containing the interval limits as closed intervals on both extremes. None if more intervals than data where asked.
        :rtype: List

        .. todo:: create exception, for example to use in this method
        .. todo:: review parameters
        """
        
        # Prepare data for precision, erase duplicates and sort data
        data = sorted(list(set([round(i, precision) for i in data])))

        # If intervals is greater than the number of different data -1, return None
        if len(data)-1<intervals or intervals<1:
            return None

        # If intervals is 1, return the data set
        if intervals==1:
            return [[data[0],data[-1]]]
        
        # Dummy best candidate
        bestFinal = {"intervals": [], "gvf": 0}
        bestIterations = 0

        # This is the start of a consecutive search for a best solution
        while bestIterations<bestOf:

            # Initial population: a bunch of different random intervalization
            population = []
            for p in range(0, initialPopulation):
                # First slice point within the dataset
                slicePoints = [random.randint(0, random.randint(1,len(data)-intervals))]

                # Based on the first one, the intermediate
                [slicePoints.append(random.randint(slicePoints[i-1]+1, len(data)-intervals+i)) \
                for i in range(1, intervals)]

                # Final random intervals
                # First
                slices = [data[0:slicePoints[0]+1]]

                # Intermediate ones
                [slices.append(data[slicePoints[i]+1:slicePoints[i+1]+1]) \
                for i in range(0, len(slicePoints)-2)]

                # Last one
                slices.append(data[slicePoints[-2]+1:])

                # Append to population
                population.append({"intervals": slices, "gvf": self._gvf(data, slices)})
            
            generation = 0
                    
            # Iterate generations for a local optima
            while generation<generations:
                # Select the fittest among the current population
                best = sorted([i["gvf"] for i in population], reverse=True)[0:bestPopulation]
                population = [i for i in population if i["gvf"] in best]

                # Create a new population for mutated childrens
                newPopulation = []

                # Iterate current population for mutated childrens
                for i in population:
                    # Generate mutated childrens for current solution
                    for m in range(0, mutatedChildrens):
                        # Copy father
                        inter = copy.deepcopy(i["intervals"])

                        # Initiate mutation sequence
                        for n in range(0, maxMutations):
                            index = random.randint(0,len(inter)-1)
                            side = random.randint(0,1)
                            self._switchElement(inter, index, side)

                        # Add new mutated children to the new population
                        candidate = {"intervals": inter, "gvf": self._gvf(data, inter)}
                        newPopulation.append(candidate)

                # Append new population to the latter generation
                population.extend(newPopulation)

                # Iterate next generation
                generation+=1

            # Get the best of last generation
            bestGvf = sorted([i["gvf"] for i in population], reverse=True)[0]
            bestFit = [i for i in population if i["gvf"]==bestGvf][0]

            # Substitute if better
            if bestFit["gvf"]>bestFinal["gvf"]:
                bestFinal = copy.deepcopy(bestFit)
                
            bestIterations+=1
                                
        # Get the best among all iterations and all generations and prepare final
        # response as closed intervals of values
        ranges = []
        for i in bestFinal["intervals"]:
            if len(i)==1:
                ranges.append([i[0],i[0]])
            else:
                ranges.append([i[0],i[-1]])
        
        return ranges

    
    def _switchElement(self, intervals, index, leftRight):
        """
        Switch an element between intervals. Index gives the left / right
        most element to the left / right neighbour.
        leftRight is 0 for left, or 1 for rigth.
        """
        
        if leftRight==0 and index>0 and len(intervals[index])>1:
            intervals[index-1].append(intervals[index][0])
            del intervals[index][0]

        if leftRight==1 and index<len(intervals)-1 and len(intervals[index])>1:
            intervals[index+1].insert(0, intervals[index][-1])
            del intervals[index][-1]
    
            
    def _divideEvenly(self, data, intervals):
        """
        Divides data in equal intervals for an initial approach to Jenks.
        """
        size = len(data)/intervals
        out = [[0, size]]

        if intervals>1:
            for i in range(1, intervals-1):
                a = [out[i-1][1], out[i-1][1]+size]
                out.append(a)
                
            out.append([out[-1][1], len(data)])

            return [data[a[0]:a[1]] for a in out]
        else:
            return [data]

        
    def _gvf(self, data, intervals):
        """
        Calculates the goodness of fit for a group of intervals.
        """

        sdam = self._sdam(data)
        sdcm = 0

        for i in intervals:
            sdcm = sdcm+self._sdam(i)

        return (sdam-sdcm)/sdam
    

    def _sdam(self, data):
        """
        Calculates the sum of squared deviations for array mean of a list.
        """

        m = sum(data)/len(data)
        return sum([math.pow(i-m, 2) for i in data])

    
    
