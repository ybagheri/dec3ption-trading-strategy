//+------------------------------------------------------------------+
//| Dec3ptionTradingStrategy.mq5                                       |
//| Dec3ption Group-II signals: touch of Minor-Major level +           |
//| confirmation within 2 CLOSED candles -> arrow at confirmation      |
//| close. SL = level +/- buffer; TP1 = 1R.                            |
//|                                                                    |
//| Parity: identical algorithm to Python                               |
//|   src/dec3ption/strategy/indicator.py (single source of truth).     |
//|   Cross-check with tests/fixtures/parity_bars.csv +                 |
//|   tests/fixtures/parity_expected.csv (R9.2).                        |
//| Signals evaluate on CLOSED bars only (bar 0 forming is excluded)    |
//| -> confirmed arrows do not repaint (R9.1).                          |
//+------------------------------------------------------------------+
#property copyright "Dec3ption Group-II"
#property version   "1.00"
#property indicator_chart_window
#property indicator_buffers 4
#property indicator_plots   4

#property indicator_type1   DRAW_ARROW
#property indicator_color1  clrLimeGreen
#property indicator_width1  2
#property indicator_label1  "Buy"
#property indicator_type2   DRAW_ARROW
#property indicator_color2  clrRed
#property indicator_width2  2
#property indicator_label2  "Sell"
#property indicator_type3   DRAW_LINE
#property indicator_color3  clrOrange
#property indicator_style3  STYLE_DASH
#property indicator_label3  "StopLoss"
#property indicator_type4   DRAW_LINE
#property indicator_color4  clrDodgerBlue
#property indicator_style4  STYLE_DASH
#property indicator_label4  "TakeProfit1"

//--- inputs
input int    InpLookback       = 500;    // Lookback bars for level search
input double InpBufferPoints   = 10.0;   // SL buffer (points)
input int    InpMaxCloses      = 2;      // Closes beyond level before kill
input double InpDojiBodyRatio  = 0.1;    // Body/range ratio = doji (skipped)
input int    InpLevelsRayBars  = 30;     // SL/TP1 ray length (bars)
input bool   InpShowLevels     = true;   // Draw SL/TP1 rays
input int    InpArrowBuyCode   = 233;    // Buy arrow code
input int    InpArrowSellCode  = 234;    // Sell arrow code

//--- buffers
double BufBuy[];
double BufSell[];
double BufSL[];
double BufTP1[];

//+------------------------------------------------------------------+
bool IsBullMM(const double &o[], const double &h[], const double &c[], int j)
{
   if(j < 1) return false;
   return (c[j] > o[j] && c[j-1] > o[j-1] && c[j] > h[j-1]);
}
//+------------------------------------------------------------------+
bool IsBearMM(const double &o[], const double &l[], const double &c[], int j)
{
   if(j < 1) return false;
   return (c[j] < o[j] && c[j-1] < o[j-1] && c[j] < l[j-1]);
}
//+------------------------------------------------------------------+
bool IsDojiOrInside(const double &o[], const double &h[], const double &l[],
                    const double &c[], int j)
{
   if(j < 1) return false;
   double body = MathAbs(c[j] - o[j]);
   double rng  = h[j] - l[j];
   bool doji   = (rng > 0 && body / rng < InpDojiBodyRatio);
   bool inside = (h[j] <= h[j-1] && l[j] >= l[j-1]);
   return (doji || inside);
}
//+------------------------------------------------------------------+
// Most recent Minor-Major extreme at/before `end`. Returns bar index,
// level via `level`. direction: +1 buy (low), -1 sell (high).
int LastMMLevel(const double &o[], const double &h[], const double &l[],
                const double &c[], int end, int first, int direction, double &level)
{
   for(int j = end; j > first; j--)
   {
      if(direction > 0 && IsBullMM(o, h, c, j)) { level = l[j-1]; return j; }
      if(direction < 0 && IsBearMM(o, l, c, j)) { level = h[j-1]; return j; }
   }
   return -1;
}
//+------------------------------------------------------------------+
bool KilledByCloses(const double &o[], const double &h[], const double &l[],
                    const double &c[], int formed, int end, double level, int direction)
{
   int cnt = 0;
   for(int k = formed + 1; k <= end; k++)
   {
      if(IsDojiOrInside(o, h, l, c, k)) continue;
      if(direction > 0 && c[k] < level) { cnt++; if(cnt > InpMaxCloses) return true; }
      if(direction < 0 && c[k] > level) { cnt++; if(cnt > InpMaxCloses) return true; }
   }
   return false;
}
//+------------------------------------------------------------------+
int OnInit()
{
   SetIndexBuffer(0, BufBuy,  INDICATOR_DATA);
   SetIndexBuffer(1, BufSell, INDICATOR_DATA);
   SetIndexBuffer(2, BufSL,   INDICATOR_DATA);
   SetIndexBuffer(3, BufTP1,  INDICATOR_DATA);
   PlotIndexSetInteger(0, PLOT_ARROW, InpArrowBuyCode);
   PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, -15);
   PlotIndexSetInteger(1, PLOT_ARROW, InpArrowSellCode);
   PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, 15);
   PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE);
   Print("Dec3ptionTradingStrategy v1.00 init: lookback=", InpLookback,
         " bufferPts=", InpBufferPoints, " maxCloses=", InpMaxCloses);
   return INIT_SUCCEEDED;
}
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
   if(rates_total < 10) return 0;                       // insufficient history
   int lastClosed = rates_total - 2;                    // bar rates_total-1 is forming
   if(lastClosed < 3) return rates_total;

   // Full deterministic recalc -> historical stability (same data = same arrows)
   for(int i = 0; i < rates_total; i++)
   {
      BufBuy[i] = EMPTY_VALUE; BufSell[i] = EMPTY_VALUE;
      BufSL[i]  = EMPTY_VALUE; BufTP1[i]  = EMPTY_VALUE;
   }

   double buffer = InpBufferPoints * _Point;
   int first = MathMax(1, lastClosed - InpLookback);

   for(int i = first + 1; i <= lastClosed; i++)
   {
      for(int d = 0; d < 2; d++)
      {
         int direction = (d == 0 ? 1 : -1);
         double level = 0;
         int formed = LastMMLevel(open, high, low, close, i, first, direction, level);
         if(formed < 0) continue;
         if(KilledByCloses(open, high, low, close, formed, i, level, direction)) continue;
         if(!(low[i] <= level && level <= high[i])) continue;   // touch of the level
         int jEnd = MathMin(i + 2, lastClosed + 1);
         for(int j = i; j < jEnd; j++)
         {
            bool mm = (direction > 0 ? IsBullMM(open, high, close, j)
                                     : IsBearMM(open, low, close, j));
            if(!mm) continue;
            double entry = close[j];
            double sl = (direction > 0 ? level - buffer : level + buffer);
            double risk = MathAbs(entry - sl);
            double tp1 = (direction > 0 ? entry + risk : entry - risk);
            if(direction > 0) BufBuy[j] = low[j] - 15 * _Point;
            else              BufSell[j] = high[j] + 15 * _Point;
            if(InpShowLevels)
            {
               int rayEnd = MathMin(j + InpLevelsRayBars, lastClosed);
               for(int b = j; b <= rayEnd; b++) { BufSL[b] = sl; BufTP1[b] = tp1; }
            }
            break;   // first trigger per touch wins
         }
      }
   }
   return rates_total;
}
//+------------------------------------------------------------------+
