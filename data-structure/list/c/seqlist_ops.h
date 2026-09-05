#ifndef SEQLIST_OPS_H
#define SEQLIST_OPS_H

#include <stddef.h>
#include "seqlist.h"


/* Remove the minimum element from L (assuming it is unique)
 * The removed value is returned via min_value
 * The vacated position is filled by the last element
 */

Status DeleteMin(SqList *L, ElemType *min_value);
Status Reverse(SqList *L);

#endif
