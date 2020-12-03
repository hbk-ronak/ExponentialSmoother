# ExponentialSmoother

The objective of this project is to write a collection of Python functions which you will use to
clean and smooth data. 

1. A function that will properly clean and index data. This function should:
   - Allow the user to pass an option that will delete trades of a certain type.
   - Allow the user to pass an option that will allow the user to specify the time period over which the data to be extracted will reside. For example, all data from 9:30 to 4:00.
2. Write a function that will accept a collection of DataFrames and return a db structure as seen in lecture.
   - Allow the user to pass an option that specifies the data type to be used in the db structure. For example, log returns, price, volume, etc.
3. Write a function to perform exponential smoothing on a data set. The function should be able to smooth time series which are scalars, vectors, or matrices.
